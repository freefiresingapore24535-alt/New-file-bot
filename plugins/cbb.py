# Copyright (C) 2025
# Codeflix-Bots@Github - MIT License

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from bot import Bot
from config import *
from database.database import db


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    # ========================= HOME ========================= #
    if data == "home":

        buttons = [
            [
                InlineKeyboardButton("• ᴀʙᴏᴜᴛ •", callback_data="about"),
                InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close"),
            ],
            [
                InlineKeyboardButton(
                    "• ᴅᴇᴠᴇʟᴏᴘᴇʀ •", url="https://t.me/Minato_Sencie"
                )
            ],
        ]

        # Admin button from config.py
        if query.from_user.id in ADMINS:
            buttons.insert(
                0,
                [
                    InlineKeyboardButton(
                        "⛩️ ᴄᴏᴍᴍᴀɴᴅꜱ ⛩️", callback_data="help"
                    )
                ],
            )

        await query.message.edit_text(
            text=START_MSG.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    # ========================= ABOUT ========================= #
    elif data == "about":
        await query.message.edit_text(
            text=ABOUT_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("• ʜᴏᴍᴇ •", callback_data="home"),
                        InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close"),
                    ],
                    [
                        InlineKeyboardButton(
                            "• ᴅᴇᴠᴇʟᴏᴘᴇʀ •",
                            url="https://t.me/Minato_Sencie",
                        )
                    ],
                ]
            ),
        )

    # ========================= HELP ========================= #
    elif data == "help":
        await query.message.edit_text(
            text=CMD_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("• ʜᴏᴍᴇ •", callback_data="home"),
                        InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close"),
                    ],
                    [
                        InlineKeyboardButton(
                            "• ᴅᴇᴠᴇʟᴏᴘᴇʀ •",
                            url="https://t.me/Minato_Sencie",
                        )
                    ],
                ]
            ),
        )

    # ========================= PREMIUM ========================= #
    elif data == "premium":

        await query.message.delete()

        await client.send_photo(
            chat_id=query.message.chat.id,
            photo=QR_PIC,
            caption=(
                f"<b>ʜᴇʏ!! {query.from_user.first_name}\n\n<\b>"
                f"𝙃𝙚𝙮 𝙜𝙪𝙮𝙨...\n"
                f"𝙔𝙤𝙪 𝙬𝙖𝙣𝙩 𝙨𝙢𝙤𝙤𝙩𝙝 𝙚𝙭𝙥𝙚𝙧𝙞𝙚𝙣𝙘𝙚...\n"
                f"𝙉𝙤 𝙢𝙤𝙧𝙚 𝙫𝙚𝙧𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣...\n"
                f"𝘽𝙪𝙮 𝙤𝙪𝙧 𝙥𝙧𝙚𝙢𝙞𝙪𝙢 𝙨𝙪𝙧𝙫𝙞𝙘𝙚...\n\n"
                f"<blockquote>🎖️ ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴꜱ<\blockquote>\n"
                f"<b>◉ 7 ᴅᴀʏꜱ :- {PRICE1}\n<\b>"
                f"<b>◉ 1 ᴍᴏɴᴛʜ  :- {PRICE2}\n<\b>"
                f"<b>◉ 3 ᴍᴏɴᴛʜ  :- {PRICE3}\n<\b>"
                f"<b>◉ 6 ᴍᴏɴᴛʜ  :- {PRICE4}\n<\b>"
                f"<b>◉ 1 ʏᴇᴀʀ :- {PRICE5}\n<\b>"
                f"•─────•─────────•─────•\n"
                f"𝘿𝙢 𝙢𝙚:- <a href='https://t.me/Minato_Sencie'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⏤͟͞ 𝙈𝙞𝙣𝙖𝙩𝙤ˢᵉⁿᶜᶦᵉ",
                            url=SCREENSHOT_URL,
                        )
                    ],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")],
                ]
            ),
        )

    # ========================= CLOSE ========================= #
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    # ========================= RFS — CHANNEL PAGE ========================= #
    elif data.startswith("rfs_ch_"):
        cid = int(data.split("_")[2])

        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            new_mode = "off" if mode == "on" else "on"

            buttons = [
                [
                    InlineKeyboardButton(
                        f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}",
                        callback_data=f"rfs_toggle_{cid}_{new_mode}",
                    )
                ],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")],
            ]

            await query.message.edit_text(
                f"Channel: {chat.title}\nForce-Sub: {'🟢 ON' if mode == 'on' else '🔴 OFF'}",
                reply_markup=InlineKeyboardMarkup(buttons),
            )

        except Exception:
            await query.answer(
                "Failed to fetch channel info", show_alert=True
            )

    # ========================= RFS — TOGGLE MODE ========================= #
    elif data.startswith("rfs_toggle_"):
        cid = int(data.split("_")[2])
        action = data.split("_")[3]

        mode = "on" if action == "on" else "off"

        await db.set_channel_mode(cid, mode)
        await query.answer(f"Force-Sub set to {mode.upper()}")

        chat = await client.get_chat(cid)
        new_mode = "off" if mode == "on" else "on"

        buttons = [
            [
                InlineKeyboardButton(
                    f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}",
                    callback_data=f"rfs_toggle_{cid}_{new_mode}",
                )
            ],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")],
        ]

        await query.message.edit_text(
            f"Channel: {chat.title}\nForce-Sub: {'🟢 ON' if mode == 'on' else '🔴 OFF'}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    # ========================= RFS — BACK ========================= #
    elif data == "fsub_back":
        channels = await db.show_channels()
        buttons = []

        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append(
                    [
                        InlineKeyboardButton(
                            f"{status} {chat.title}",
                            callback_data=f"rfs_ch_{cid}",
                        )
                    ]
                )
            except:
                continue

        await query.message.edit_text(
            "Select channel to toggle Force-Sub:",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
