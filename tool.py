import bs4
import praw
import requests

reddit = praw.Reddit("gpmods")

year = int(input("Current in-game year: "))
while True:
    action = int(input("0 to check credentials, 1 to post UN proposals, 2 to post UN voting, 3 to post UN results, 4 to exit: "))
    if action == 0:
        try:
            reddit.user.me()
            print("Credentials valid")
        except:
            print("Credentials invalid")
    elif action == 1:
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
        link = input("Proposals link: ")
        id = praw.models.Submission.id_from_url(link)
        post = reddit.submission(id=id)
        post.comments.replace_more()
        claims = requests.get("https://www.reddit.com/r/GlobalPowers/wiki/list").text
        claims = list(bs4.BeautifulSoup(claims, "html.parser").stripped_strings)
        reso_unga, reso_unsc = [], []
        if len(claims) < 100:
            print("Reddit is broken, try again later")
            continue
        for comment in post.comments.list():
            if comment.author.name == "GPMods" and "General Assembly" in comment.body:
                for reply in comment.replies:
                    if isinstance(reply, praw.models.Comment):
                        try:
                            if claims.index("/u/" + reply.author.name) != -1 and claims.index("/u/" + reply.author.name) < claims.index("Bougainville"): # standin for no recognition
                                reso_unga.append(reply.body)
                            else:
                                reply.reply("You are not authorised to propose this resolution. If you believe this is a mistake, please contact the moderators.")
                        except:
                            reply.reply("You are not authorised to propose this resolution. If you believe this is a mistake, please contact the moderators.")
            elif comment.author.name == "GPMods" and "Security Council" in comment.body:
                for reply in comment.replies:
                    if isinstance(reply, praw.models.Comment):
                        try:
                            if claims.index("/u/" + reply.author.name) != -1 and claims.index("/u/" + reply.author.name) < claims.index("Bougainville") and claims[claims.index("/u/" + reply.author.name) - 2] in post.selftext: # standin for no recognition and unsc
                                reso_unsc.append(reply.body)
                            else:
                                reply.reply("You are not authorised to propose this resolution. If you believe this is a mistake, please contact the moderators.")
                        except:
                            reply.reply("You are not authorised to propose this resolution. If you believe this is a mistake, please contact the moderators.")
        backslashes = "\n\n"
        text = f"""This is the {year} United Nations voting thread. You can just comment "vote" under the "yes", "no", or "abstain" options. Only [UNSC members]({link}) may vote on the UNSC resolutions, and voting for new UNSC members will be done in a separate comment.\n\n**General Assembly Resolutions**\n\n{backslashes.join(reso_unga)}\n\n**Security Council Resolutions**\n\n{backslashes.join(reso_unsc)}"""
        post = reddit.subreddit("GlobalPowers").submit(f"[UN] United Nations {year} Voting", selftext=text)
        comment1 = post.reply("**General Assembly Resolutions**")
        comment1.mod.distinguish(how="yes", sticky=True)
        comment2 = post.reply("**Security Council Resolutions**")
        comment2.mod.distinguish(how="yes", sticky=False)
        for i in range(len(reso_unga)):
            reso = comment1.reply(f"**A/RES/{year - 1946}/{i + 1}**: {reso_unga[i]}")
            reso.reply("Yes")
            reso.reply("No")
            reso.reply("Abstain")
        for i in range(len(reso_unsc)):
            reso = comment2.reply(f"**S/RES/{year - 1946}/{i + 1}**: {reso_unsc[i]}")
            reso.reply("Yes")
            reso.reply("No")
            reso.reply("Abstain")
        print(post.url)
    elif action == 3:
        print("The voting rules are too complex to be simulated by a program.")
        raise NotImplementedError
    elif action == 4:
        raise SystemExit