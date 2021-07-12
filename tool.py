import praw

reddit = praw.Reddit("gpmods")

while True:
    action = int(input("0 to check credentials, 1 to post UN proposals, 2 to post UN voting, 3 to post UN results, 4 to exit: "))
    if action == 0:
        try:
            reddit.user.me()
            print("Credentials valid")
        except:
            print("Credentials invalid")
    elif action == 1:
        year = int(input("Current year: "))
        perm_unsc, temp_unsc = ["China", "France", "Russian Federation", "United Kingdom", "United States"], []
        while (member := input("Temporary UNSC members (e to exit): ")) != "e":
            temp_unsc.append(member)
        text = f"""**United Nations Security Council**\n\n**Permanent Members**: {", ".join(perm_unsc)}\n\n**Temporary Members**: {", ".join(temp_unsc)}\n\n---\n\nPost United Nations proposals for {year} below. Only UNSC members can make UNSC proposals."""
        post = reddit.subreddit("GlobalPowers").submit(f"[UN] United Nations {year} Proposals", selftext=text)
        comment1 = post.reply("Post **General Assembly** resolutions here, with **one resolution** per comment.")
        comment1.mod.distinguish(how="yes", sticky=True)
        comment2 = post.reply("Post **Security Council** resolutions here, with **one resolution** per comment.")
        comment2.mod.distinguish(how="yes", sticky=False)
        print(post.url)
    elif action == 2:
        raise NotImplementedError
    elif action == 3:
        raise NotImplementedError
    elif action == 4:
        raise SystemExit