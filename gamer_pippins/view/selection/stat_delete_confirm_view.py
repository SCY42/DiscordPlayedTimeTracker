def statDeleteConfirmView(games: list[str]):
    view = discord.ui.View()
    view.add_item(StatDeleteYesButton(games, view))
    view.add_item(StatDeleteNoButton(games, view))

    return view