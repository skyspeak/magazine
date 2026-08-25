# -*- coding: utf-8 -*-
"""Emits the ten kid cards (Nos. 02-11) as an HTML fragment.
The fragment was assembled once into kids/no-02-11-ten-things-to-ask-for.html,
which is the source of truth. Edit CARDS here to regenerate the fragment."""
CARDS=[
 dict(n="02",t="A phone",c="pink",
  scared="You disappearing into it.",
  say="Can we start with one that just calls and texts?",
  dont="&ldquo;Everyone has one.&rdquo; They know. It has never once worked.",
  job="Put it in the kitchen at night before they ask you to.",
  notyet="Ask what you&rsquo;d have to show them. Then show them, for a month."),
 dict(n="03",t="Being online",c="blue",
  scared="Strangers, and stuff that never goes away.",
  say="You can follow my account. I&rsquo;d rather you saw it than found it.",
  dont="&ldquo;You don&rsquo;t get it.&rdquo; Maybe not. Doesn&rsquo;t help you.",
  job="Tell them one thing that happened online before they hear it from someone else.",
  notyet="Ask for a group chat with people you both know."),
 dict(n="04",t="A sleepover",c="yellow",
  scared="You at 1am, in a house they&rsquo;ve never been in.",
  say="If I want to come home I&rsquo;ll text you. I won&rsquo;t be embarrassed.",
  dont="&ldquo;I&rsquo;ll be fine!&rdquo; Then at 1am you&rsquo;re stuck being fine.",
  job="Pick a code word together. Boring. Works.",
  notyet="Ask for a late&#8209;over. All the fun, home at nine."),
 dict(n="05",t="Going on your own",c="green",
  scared="Roads. Honestly, mostly roads.",
  say="Can we walk it together three times first?",
  dont="&ldquo;Nothing&rsquo;s going to happen.&rdquo; You can&rsquo;t promise that.",
  job="Say out loud what you&rsquo;d do if the shop&rsquo;s shut and your phone&rsquo;s dead. Before they ask.",
  notyet="Ask for half the route."),
 dict(n="06",t="Quitting",c="pink",
  scared="That you&rsquo;ll quit everything from now on.",
  say="I want to stop at the end of term. Not today.",
  dont="&ldquo;I hate it.&rdquo; That&rsquo;s a noise, not information.",
  job="Work out which bit you hate: the thing, the person, or the practising. Three different problems.",
  notyet="Ask to change one thing and try three more weeks."),
 dict(n="07",t="Staying home alone",c="blue",
  scared="The doorbell. And you not picking up.",
  say="Give me twenty minutes while you get milk.",
  dont="&ldquo;I&rsquo;m not a baby.&rdquo; True. Still annoying.",
  job="Answer your phone. Every time. Miss it once and this gets very slow.",
  notyet="Ask for ten minutes while they&rsquo;re in the garden."),
 dict(n="08",t="Your own money",c="yellow",
  scared="Paying for the same thing twice.",
  say="If I buy something rubbish, don&rsquo;t replace it.",
  dont="&ldquo;Can I have it early?&rdquo; Not once. Ever.",
  job="Save for one thing all the way to the end, where they can watch you do it.",
  notyet="Ask for less, weekly, in cash."),
 dict(n="09",t="A job",c="green",
  scared="Your sleep.",
  say="Cap my hours, and check my grades in a month.",
  dont="&ldquo;It won&rsquo;t affect anything.&rdquo; It will. Say so first.",
  job="Make the phone calls yourself. Including the awkward one.",
  notyet="Ask to do one paid thing first. Babysitting. Someone&rsquo;s garden."),
 dict(n="10",t="How you look",c="pink",
  scared="Only the permanent ones. That&rsquo;s genuinely it.",
  say="This one washes out. Can that one be mine?",
  dont="&ldquo;It&rsquo;s my body.&rdquo; True. Still loses the argument.",
  job="Split your list into grows&#8209;back and doesn&rsquo;t. Ask for the grows&#8209;back ones first.",
  notyet="Get a date for the permanent one. Then drop it until then."),
 dict(n="11",t="Going out with someone",c="blue",
  scared="You telling them nothing at all.",
  say="Do you want to meet them?",
  dont="Saying nothing. Silence makes grown&#8209;ups invent things.",
  job="Tell them one boring true thing early. It buys you privacy about the rest.",
  notyet="Ask exactly what&rsquo;s allowed right now. Exactly."),
]
row=lambda k,v: f'<div class="row"><span class="k">{k}</span><span class="v">{v}</span></div>'
chips=[];cards=[]
for c in CARDS:
    chips.append(f'<a class="chip {c["c"]}" href="#c{c["n"]}">{c["t"]}</a>')
    cards.append(f'''
<article class="card {c["c"]}" id="c{c["n"]}">
  <div class="chead"><span class="cn marker">{c["n"]}</span><h2 class="marker">{c["t"]}</h2></div>
  {row("They&rsquo;re scared of", c["scared"])}
  <div class="row"><span class="k">Say</span><span class="v bub">{c["say"]}</span></div>
  {row("Don&rsquo;t say", c["dont"])}
  {row("Your job", "<b>"+c["job"]+"</b>")}
  {row("If they say not yet", c["notyet"])}
</article>''')
open("kid_body.html","w").write(
  '<nav class="chips" aria-label="Jump to an ask">'+"".join(chips)+'</nav>\n'+"\n".join(cards))
print("cards:",len(CARDS))
