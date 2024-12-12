from ..board_manager import BoardManager as BM
from ..chatbot import Chatbot
from ..cookies import cookieProperties as cookies
from ..db import DBSessions as DBS, DBBoard as DBB, DBGlobal as DBG
from datetime import datetime
from ..environment import Environment
from fastapi import (
    APIRouter,
    Form,
    Request,
)
from fastapi.responses import JSONResponse, Response
from fastapi.templating import Jinja2Templates
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


def get_client_ip(request: Request) -> str:
    """Get actual client ip address including forwarding"""
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    logger.info(f"X-Forwarded-For: {x_forwarded_for}")
    if x_forwarded_for:
        # The first IP in the list is the original client IP
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.client.host
    return ip


def check_if_user_logged_in(request):
    dbg_config = DBG.get_config()

    # Check for chatbot_id
    cookie_chatbot_id = request.cookies.get(f"{cookies.login_cookie_prefix}id")
    if not cookie_chatbot_id:
        return False
    dbg_chatbot_id = dbg_config.get("chatbot_id")
    logger.info(f"Comparing chatbot_id: {cookie_chatbot_id} vs. {dbg_chatbot_id}")
    if cookie_chatbot_id != dbg_chatbot_id:
        return False

    # user ip comparison deactivated
    # # check for user_ip
    # user_ip = get_client_ip(request)
    # cookie_chatbot_userip = request.cookies.get(f"{login_cookie_prefix}userip")
    # logger.info(f"Comparing user_ip: {cookie_chatbot_userip} vs. {user_ip}")
    # if cookie_chatbot_userip != user_ip:
    #     return False

    return True


@router.get("/")
async def root_get(request: Request):
    dbg_config = DBG.get_config()

    # check if intro should be skipped
    skip_intro = dbg_config.get("skip_intro") == 1
    if skip_intro:
        logger.debug("skipping login page: redirecting to chat.html")
        # pre-configure chatbot
        username = "User"
        useremail = "nan"
    elif logged_in := check_if_user_logged_in(request):
        logger.debug("user logged in: redirecting to chat.html")
        username = request.cookies.get(f"{cookies.login_cookie_prefix}username", "User")
        useremail = request.cookies.get(
            f"{cookies.login_cookie_prefix}useremail", "nan"
        )

    if skip_intro or logged_in:
        form_data = dict(
            username=username,
            useremail=useremail,
            ip=get_client_ip(request),
            password=request.app.state.password,
        )
        return await root_post(request, **form_data)
    else:
        # intro text
        intro_wide = dbg_config.get("intro_wide")
        intro_narrow = dbg_config.get("intro_narrow")

        # get templates
        templates = Jinja2Templates(
            directory=Path(__file__).resolve().parent / Path("../../frontend/templates")
        )

        # get app.root_path
        root_path = Environment.get_app_root_path(dbg_config.get("port"))

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "botname": dbg_config.get("bot_name"),
                "intro_wide": intro_wide,
                "intro_narrow": intro_narrow,
                "form_post_url": root_path,
                "password_required": request.app.state.password is not None,
            },
        )


@router.post("/")
async def root_post(
    request: Request,
    username: str = Form(...),
    useremail: str = Form("nan"),
    password: str = Form(None),
    ip: str = Form("nan"),
):
    """
    Serves the chat template with default values for a session without login.
    """
    if request.app.state.password and password != request.app.state.password:
        logger.info("Wrong password")
        return JSONResponse(status_code=401, content={"detail": "Wrong password"})

    logger.info("Serving chat.html")
    templates = Jinja2Templates(
        directory=Path(__file__).resolve().parent / Path("../../frontend/templates")
    )

    session_data = dict(
        username=username,
        useremail=useremail,
        userip=ip,
    )

    # add new session, board, and chatbot configuration to database
    session_id = DBS.add_session(**session_data)

    dbg_config = DBG.get_config()
    board_path = dbg_config.get("instance_board_path")
    board = BM.get_board(path=board_path, as_dict=True)
    bm_config = BM.get_chain_parameters(
        path=board_path,
        current_bot_card_id=dbg_config.get("current_card_id"),
    )
    bm_config["bot_name"] = dbg_config.get("bot_name")
    bm_config["username"] = username
    DBB.add_board(session_id, board, dbg_config.get("current_card_id"))
    Chatbot.setup(session_id, bm_config)

    c = DBG.get_config()
    port = c.get("port")
    response = templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "timestamp": datetime.now().strftime("%Y.%m.%d, %H:%M:%S"),
            "botname": bm_config.get("bot_name"),
            "initial_prompt": bm_config.get("initial_prompt"),
            "initial_response": bm_config.get("initial_response"),
            "username": username,
            "ws_text_url": Environment.get_websocket_url(port),
            "ws_audio_url": Environment.get_websocket_url(port),
            "app_url": (
                Environment.get_app_url(port) if not Environment._is_local() else "/"
            ),
            "show_function_calls": True,
        },
    )

    do_login(response, **session_data)

    # Store the session id in a cookie
    response.set_cookie(
        key=f"{cookies.login_cookie_prefix}session_id",
        value=session_id,
        path=cookies.login_cookie_path,
        samesite="None",
        secure=True
    )
    return response


@router.post("/logout")
async def logout_post():
    response = Response()
    do_logout(response)
    return response


def do_login(response: Response, **login_data):

    for key, value in cookies.login_cookies.items():
        if key in login_data:
            value = login_data[key]
        response.set_cookie(
            key=f"{cookies.login_cookie_prefix}{key}",
            value=value,
            path=cookies.login_cookie_path,
            max_age=cookies.max_age,
            samesite="None",
            secure=True
        )


def do_logout(response: Response):
    for key in cookies.login_cookies:
        response.set_cookie(
            key=f"{cookies.login_cookie_prefix}{key}",
            value=None,
            path=cookies.login_cookie_path,
            max_age=0,
            samesite="None",
            secure=True
        )
