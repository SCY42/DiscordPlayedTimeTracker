async def disableEveryItem(msg: discord.Message, view: discord.ui.View):
    for item in view.children:
        item.disabled = True    # type: ignore
    GAMER_PIPPINS.logger.info(f"메시지 뷰 비활성화됨. ({msg.jump_url}")
    
    await msg.edit(view=view)