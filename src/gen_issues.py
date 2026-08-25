# -*- coding: utf-8 -*-
"""Emits the ten parent issues (Nos. 02-11) as an HTML fragment.
The fragment was assembled once into parents/no-02-11-ten-more-big-asks.html,
which is the source of truth. Edit ISSUES here to regenerate the fragment."""
ISSUES = [
 dict(no="02", t="A phone", a=(10,13), band="Usually 10&ndash;13",
  thesis="A phone is not one decision, it is <b>four</b>: a device, a phone number, an open internet, and an app store. Most families hand over all four at once because they arrive in the same box. You can grant them separately, and separating them is the whole game.",
  q="Not <em>are they responsible</em>. It is: are they ready to be reachable by everybody, all the time, with no adult in the room?",
  dec=["Which of the four you are actually giving","Where it sleeps","Who is allowed to contact them"],
  fact="Whatever rule you set on day one is the rule. Adding a restriction six months later reads as a punishment for something; setting it at the start is just how phones work in this house.",
  say="You can have a phone. It is for calling and texting us and your friends. The internet and apps are a separate conversation, and we will have it in six months.",
  dont="If your grades slip I am taking it away.",
  nowhy="The moment the phone is the currency for everything else, every conversation in your house becomes a phone conversation.",
  rule="The phone sleeps outside the bedroom. Everyone&rsquo;s does, including yours.",
  rulewhy="This is the single rule that is almost impossible to introduce later and almost frictionless to start with.",
  ready=["They can be bored for ten minutes without reaching for something","They have told you about something that went wrong, unprompted, at least once","They can hand it over when asked without a scene"],
  notyet="Start with a phone that only calls and texts, and put the date for the next conversation in the calendar."),

 dict(no="03", t="Being online", a=(12,15), band="Usually 12&ndash;15",
  thesis="This is not a screen&#8209;time decision, it is an <b>audience</b> decision. You are deciding whether your child gets a public &mdash; a room of people they cannot see, that keeps a copy of everything.",
  q="Not <em>how long are they on it</em>. It is: who can see them, who can message them, and what happens to it afterwards?",
  dec=["Public or private","Who can send them a message","Whether you are in the audience"],
  fact="Thirteen is the platforms&rsquo; own minimum, and it is a legal floor rather than a recommendation. Nothing posted is ever really retrievable, including the things deleted nine seconds later.",
  say="One condition. I get to see it. Not to police you &mdash; because you are thirteen and I am not sending you into a room full of adults without knowing what the room is like.",
  dont="Give me your phone. Now.",
  nowhy="Surprise inspections buy you one afternoon of information and cost you every future disclosure. Visibility agreed in advance costs nothing.",
  rule="The first account is private, and you are in the audience. Renegotiate on a named date, not on a good mood.",
  rulewhy="Private-by-default is easy on day one and a humiliation to impose in month six.",
  ready=["They can describe what they would do if a stranger messaged them","They have told you about something upsetting online before you found it yourself","They understand that deleting is not undoing"],
  notyet="A group chat with people you both know, first. It is the same skills with a knowable room."),

 dict(no="04", t="A sleepover", a=(6,10), band="Usually 6&ndash;10",
  thesis="The question is almost never whether your child is ready. It is whether <b>you know the house</b> &mdash; and whether your kid can get out of it at one in the morning without feeling like a failure.",
  q="Not <em>are they old enough</em>. It is: do I know this home, and does my kid have a working exit?",
  dec=["Whose house, and which adults are there all night","Who else is staying","What the pickup plan is"],
  fact="The failure mode is not drama. It is a quiet child at 1 a.m. who has decided that asking to go home would be embarrassing, and who says nothing for five hours.",
  say="Two things and then yes. I am going to ring their mum and ask a few boring questions. And you can come home at any hour, no embarrassment, no questions until morning. That is not failing. That is the deal.",
  dont="You&rsquo;ll be fine!",
  nowhy="Reassurance sounds kind and quietly forecloses the sentence you most need them to be able to say, which is <em>I am not fine</em>.",
  rule="A code word, and a no&#8209;questions pickup. One text, you drive, nobody discusses it until the morning.",
  rulewhy="A child will use an escape hatch they are certain costs them nothing. They will not use one they have to argue for.",
  ready=["They can phone you themselves","They have done a late evening at the house and come home at nine","They have said &lsquo;I don&rsquo;t like this&rsquo; to an adult who is not you"],
  notyet="A late&#8209;over. All of the party, collected at nine, and nobody has to be brave about it.",
  extra="<strong>The boring questions, for the other parent:</strong> who is home overnight, who else is staying, what the screen and film rules are, where everyone sleeps, and &mdash; asked plainly, the way you would ask about a swimming pool &mdash; whether there are guns in the house and how they are stored."),

 dict(no="05", t="Going somewhere alone", a=(8,12), band="Usually 8&ndash;12",
  thesis="Independence is not a switch you flip at a certain age. It is a <b>distance</b>, and you extend it. The question is never the world in general &mdash; it is this route, at this hour, with this child.",
  q="Not <em>is the world safe</em>. It is: does my kid have the judgment for this specific journey, and do they know what to do when it goes wrong?",
  dec=["Which route, at what time","What happens when plan A fails","How they tell you they arrived"],
  fact="The risk on a walk to school is overwhelmingly traffic, not strangers. So rehearse the road, not the fear &mdash; a long warning about strangers reliably raises anxiety without raising a single skill.",
  say="We are going to walk it together three times. Then you walk it while I wait at the other end. Then you do it on your own. And before any of that, tell me what you would do if the shop is shut.",
  dont="Nothing is going to happen.",
  nowhy="It is a promise you cannot keep, and it teaches them that surprises are outside the plan rather than part of it.",
  rule="Name the failure plan out loud before the first solo trip. Shop shut, friend not there, phone dead, feels wrong.",
  rulewhy="Confidence comes from having somewhere to go when the plan breaks, not from being told it will not.",
  ready=["They cross the worst road correctly without being reminded","They know an address and a phone number by heart","They have solved one small problem on their own and told you about it"],
  notyet="Shorten the leg. Half the route, or the same route at a busier hour, is a real yes rather than a soft no."),

 dict(no="06", t="Quitting the thing", a=(7,16), band="Any age, repeatedly",
  thesis="The most useful question is not whether to let them quit. It is whether they are quitting the activity or <b>quitting a bad week</b> &mdash; and those need opposite answers.",
  q="Not <em>do we allow quitting</em>. It is: which part do they actually hate &mdash; the thing, the person, or the practising? Those are three different problems with three different fixes.",
  dec=["Quit, change teacher or team, or change the amount","When the exit happens","What they owe the other people involved"],
  fact="The urge to quit usually peaks just before competence, not at the start. The plateau &mdash; where effort stops producing visible improvement &mdash; is the most common place a child asks to stop.",
  say="You can quit. Not today &mdash; at the end of term, so you are leaving from a decision instead of a bad Tuesday. And I want to know which part you hate, because if it is the teacher we have a much easier problem.",
  dont="We don&rsquo;t quit things in this family.",
  nowhy="It teaches that stopping anything is a defect of character, which is exactly the belief that keeps a twenty&#8209;six&#8209;year&#8209;old in a job they hate.",
  rule="Quit at a boundary, not in a bad moment &mdash; and finish what other people are counting on.",
  rulewhy="The lesson worth keeping is not persistence. It is that you exit cleanly and you do not leave a team short.",
  ready=["They can name the specific part they hate","They have tried one change &mdash; different teacher, different level, less of it","They have said it calmly, more than once, across several weeks"],
  notyet="Three more weeks with one thing changed, and a promise that you will honour whatever they say at the end of it. Then honour it."),

 dict(no="07", t="Staying home alone", a=(9,13), band="Usually 9&ndash;13",
  thesis="You are not really assessing whether they can be trusted alone. You are assessing <b>what they do when something goes wrong</b> &mdash; and the things that go wrong are far more boring than the ones you are picturing.",
  q="Not <em>are they mature enough</em>. It is: do they know what to do about the doorbell, the smoke alarm, the locked door, and not being able to reach me?",
  dec=["How long, and how often","Whether a sibling counts as company or as a second job","What is off limits &mdash; oven, bath, front door"],
  fact="First&#8209;time&#8209;alone problems are almost always mundane: a delivery, a locked door, a burnt slice of toast setting off an alarm, a sibling fight. Rehearse those four and you have covered most of it.",
  say="Twenty minutes while I get milk. Before I go: tell me what you do if someone knocks, if you get locked out, and if you ring me and I do not pick up.",
  dont="Just don&rsquo;t open the door to anyone.",
  nowhy="A single rule with no plan behind it. They need a script for the four boring emergencies, not one prohibition.",
  rule="Start at twenty minutes, and come back exactly when you said you would.",
  rulewhy="The first reliability being tested here is yours. A parent who is late by an hour teaches the house that stated times are approximate.",
  ready=["They can be alone and bored without ringing you five times","They follow a rule you are not there to enforce","They can call an adult who is not you"],
  notyet="Alone in the house while you are in the garden, then while you are at the end of the street. Ladder it."),

 dict(no="08", t="Money of their own", a=(7,14), band="Usually 7&ndash;14",
  thesis="The decision is not how much. It is whether you are giving them money, or giving them <b>the right to make a bad purchase</b> &mdash; because only the second one teaches anything.",
  q="Not <em>what is the right amount</em>. It is: am I actually going to let them lose it?",
  dec=["The amount, and how often","Whether it is tied to chores","Whether you get a veto"],
  fact="Money only teaches when it can be lost. An allowance that gets topped up after a bad decision is a lesson that has been deleted, at full price.",
  say="It is yours. I will tell you once if I think something is a bad idea, and then I will stop. And I am not going to replace it. That is the entire point of it being yours.",
  dont="Everything is paid, per chore.",
  nowhy="Pricing every job puts a market rate on things that should be free, and you will find yourself negotiating a fee for a child to carry their own plate.",
  rule="Let them buy the rubbish thing.",
  rulewhy="A twenty&#8209;pound regret at nine is the cheapest financial education that exists anywhere, and it does not go on a credit record.",
  ready=["They can wait a week for something they want","They can tell you roughly what things cost","They have saved for one thing all the way to the end"],
  notyet="A smaller amount, weekly, in cash, where they can physically watch it leave."),

 dict(no="09", t="A first job", a=(13,17), band="Usually 13&ndash;17",
  thesis="The money is the least interesting part. The real curriculum is <b>having a boss who is not a parent</b> &mdash; someone who corrects them, and whom they have to say no to.",
  q="Not <em>do they need the money</em>. It is: whose time is it now, and what happens the first time work and school collide?",
  dec=["An hours cap, in writing","The school&#8209;night rule","What happens to the money"],
  fact="School performance generally holds up to somewhere around ten to fifteen hours a week and starts to slide after that. Agree the cap before the first shift, not after the first bad report.",
  say="Yes. The cap is twelve hours, nothing after nine on a school night, and we look at it again in a month. What you earn is yours &mdash; I would like some of it to go somewhere it can sit.",
  dont="I&rsquo;ll ring your manager and sort the rota.",
  nowhy="You have just removed the only part of the job that was going to teach them something.",
  rule="They make the phone calls. Including the awkward one where they cannot work Saturday.",
  rulewhy="Asking an adult who is not related to you for something, out loud, is the skill. Everything else is logistics.",
  ready=["They can wake themselves up","They can be corrected without it ruining the day","They can turn down a shift without you in the room"],
  notyet="One&#8209;off paid work first &mdash; babysitting, a neighbour&rsquo;s garden, a weekend of something. Same lesson, no rota."),

 dict(no="10", t="Changing how they look", a=(10,16), band="Usually 10&ndash;16",
  thesis="Sort every single request onto one axis and most of the argument disappears: <b>grows back, washes out, or does not.</b> Hair grows. Dye fades. Most holes close. Tattoos do not.",
  q="Not <em>do I like it</em>. It is: is this reversible, and if it is, why am I in the conversation at all?",
  dec=["Which column it falls in","Any school or uniform rule that actually exists","Who pays"],
  fact="Almost every fight in this category is about a reversible thing. Parents spend their authority on hair colour and then have none left for the permanent list.",
  say="My rule is simple. If it grows back or washes out, it is your call. If it does not, we wait until you are sixteen &mdash; and then it is still your call.",
  dont="What will your grandmother say?",
  nowhy="It moves the decision from their body to other people&rsquo;s opinions, and it converts a small aesthetic choice into a fight about control, which they will win eventually anyway.",
  rule="Reversible is theirs. Save your no for the permanent list.",
  rulewhy="You get a limited number of vetoes. Spending one on green hair is a poor allocation.",
  ready=["It grows back or washes out &mdash; in which case say yes and move on","There is no actual school rule against it, only an assumption","They have wanted it for longer than a fortnight"],
  notyet="For permanent things: a date, not a lecture. And say plainly that the answer at that date is very likely yes."),

 dict(no="11", t="Going out with someone", a=(13,17), band="Usually 13&ndash;17",
  thesis="This one arrives whether or not you decided anything. So the real decision is not permission. It is whether they will <b>tell you anything</b> once it has started.",
  q="Not <em>should I allow this</em>. It is: am I someone they can report to without a scene?",
  dec=["What &lsquo;going out&rsquo; is allowed to mean right now, specifically","Where, and with how many other people around","What you actually need to know"],
  fact="The information channel is worth more than any rule you can set. Children who expect a calm reaction tell their parents things. Children who expect a scene stop reporting, and you find out much later.",
  say="I would like to meet them. Not to interrogate anybody &mdash; I just want a face to go with the name. And I promise not to make it weird.",
  dont="Ooooh, is this your <em>girlfriend</em>?",
  nowhy="Teasing at fourteen is cheap and it closes the channel for years. It is the single most expensive joke available to a parent.",
  rule="Stay unshockable. React in the morning, not in the moment.",
  rulewhy="Your face in the first four seconds decides whether they tell you the next thing.",
  ready=["This section does not really apply &mdash; it is happening","You can hear something surprising without changing your expression","They have seen you handle bad news calmly before"],
  notyet="Be specific rather than vague: what is allowed now, what is allowed at sixteen, and when you will talk about it again."),
]

def box(cls,title,inner):
    return f'<div class="box{cls}"><h3>{title}</h3>{inner}</div>'

parts=[]
toc=[]
for i in ISSUES:
    lo,hi=i["a"]
    toc.append(f'<a href="#i{i["no"]}" data-lo="{lo}" data-hi="{hi}"><b>No. {i["no"]}</b>{i["t"]}</a>')
    dec="".join(f"<li>{d}</li>" for d in i["dec"])
    rdy="".join(f"<li>{r}</li>" for r in i["ready"])
    boxes = (
      box("", "What you are actually deciding", f'<p>{i["q"]}</p><ul class="ck">{dec}</ul>')
    + box("", "The fact worth knowing", f'<p>{i["fact"]}</p>')
    + box("", "Say this, not that",
          f'<p><span class="say">{i["say"]}</span></p>'
          f'<p class="no">Not: <span class="say">{i["dont"]}</span> &mdash; {i["nowhy"]}</p>')
    + box(" rule-box", "The one rule", f'<p><strong>{i["rule"]}</strong></p><p>{i["rulewhy"]}</p>')
    + box("", "Ready when", f'<ul class="ck">{rdy}</ul>'
          f'<p style="margin-top:.6rem"><strong>If it is not yet:</strong> {i["notyet"]}</p>')
    )
    extra=f'<div class="box" style="margin-top:1.1rem">{i["extra"]}</div>' if i.get("extra") else ""
    parts.append(f'''
<article class="issue" id="i{i["no"]}" data-lo="{lo}" data-hi="{hi}">
  <div class="ihead">
    <div class="ino mono">No. {i["no"]}</div>
    <div class="ittl"><div class="iage">{i["band"]}</div><h2>So you want {i["t"].lower()}</h2></div>
  </div>
  <p class="thesis">{i["thesis"]}</p>
  <div class="grid">{boxes}</div>
  {extra}
  <div class="foot-line"><span>The Big Ask &middot; No. {i["no"]}</span><span>Decide it out loud, and decide it with them in the room</span></div>
</article>''')

open("issues_body.html","w").write(
  '<div class="toc" id="toc">'+ "".join(toc) + "</div>\n" + "\n".join(parts))
print("issues generated:",len(ISSUES))
