#!/usr/bin/env python3
# Generates the Milestones1 timeline. Emits index.html.
# Track logic: 8 coloured services at the top, one terminating at each stop,
# down to a single track at the platform.

import html, io, os

OUT = "/Users/michaelweinfeld/Documents/2026/PJ O'Rourke/Milestones1/index.html"

# ---- the eight services. index 1..8. band k terminates at stop (9-k) ----
SERVICES = [
    dict(n=1, bullet="W", name="The Work",     color="#EE352E", born="Stop 8", note="Prints, plates, the hand-to-hand sale. Runs the whole line."),
    dict(n=2, bullet="R", name="The Record",   color="#00933C", born="Stop 7", note="Dates, counts, photographs, the things only PJ knows."),
    dict(n=3, bullet="O", name="Ownership",    color="#0039A6", born="Stop 6", note="The entity, the trademarks, the copyrights."),
    dict(n=4, bullet="T", name="Trade",        color="#FF6319", born="Stop 5", note="Channels, margins, the business that pays for the rest."),
    dict(n=5, bullet="E", name="Editions",     color="#B933AD", born="Stop 4", note="Runs stated and closed. Stock becomes catalogue."),
    dict(n=6, bullet="M", name="Mission",      color="#FCCC0A", born="Stop 3", note="The foundation and what it spends the money on.", dark=True),
    dict(n=7, bullet="X", name="Exhibition",   color="#6CBE45", born="Stop 2", note="Museums, books, loans out and back."),
    dict(n=8, bullet="L", name="Licensing",    color="#996633", born="Stop 1", note="The work earning without PJ in the room."),
]

# ---- stops, page order top to bottom: Stop 1 (2075) .. Stop 8 (2012) ----
STOPS = [
    dict(
        n=1, year="Circa 2075", title="The Reissue", express=True, tag="Express &middot; Terminal",
        ann=None,
        blocks=[
            ("What this is",
             "A stencil cut in 2016 comes back. A licensed collaboration. A museum shop reprint. A capsule with a brand that didn't exist when the original sold out. People who weren't born yet buy it new and think it is new."),
            ("What to look at",
             "This isn't the goal. It's the receipt that says the goal worked. Reissues happen to artists whose work is owned, dated and defended by somebody. They don't happen to piles."),
            ("What has to be true",
             "Every design authenticated, dated and traceable to a physical plate, with one entity holding the copyright and the marks. All of that gets built further down the line."),
        ],
        listy=None,
        quote=("Art is for everybody.", "Keith Haring"),
        opens="Licensing",
    ),
    dict(
        n=2, year="Circa 2050", title="The Retrospective", express=False, tag="Local only",
        ann=None,
        blocks=[
            ("What this is",
             "A museum builds a show out of the subway work. A publisher builds a book out of the catalogue. Both call one phone number to do it, and that number is an organization."),
            ("What to look at",
             "The Express skips this stop, and it should &mdash; nobody schedules a museum show. It happens because the records are good enough that saying yes is easy. Curators go where the work is already documented. Every time."),
        ],
        listy=("What to have ready", [
            ("Loan-ready records.", "A curator asks what a piece is, when it was made and who owns it. Every answer already written down."),
            ("High-resolution files", "of every plate and print, one place, backed up twice."),
            ("One contact", "with the authority to actually grant a loan."),
        ]),
        quote=("The photographs are why the drawings still exist.", "Martha Cooper &middot; on shooting the trains in the seventies"),
        opens="Exhibition",
    ),
    dict(
        n=3, year="Circa 2032", title="The Foundation", express=True, tag="Express &middot; Major",
        ann=None,
        blocks=[
            ("What this is",
             "An organization that owns the work, licenses it, and spends the income on something PJ picks. Kids, materials, studio time, a cart for somebody else. Whatever the mission ends up saying."),
            ("What to look at",
             "Every artist worth copying built this while they were working, not at the end. Haring set his up in 1989 with a shop running and a full studio. Judd founded Chinati in 1986 and spent the next eight years using it. These were not exit plans. They were working artists deciding they would rather set the terms themselves than let somebody else do it later."),
            (None,
             "PJ has been on the platform since 2012. Fourteen years of work is not a warm-up for this. It is the qualification."),
        ],
        now=("Already on this platform",
             "ALL CITY is the mission-shaped thing. A game about the subway, carrying PJ's name and his world, "
             "is something a foundation can hand to a room full of kids without explaining it first."),
        listy=("What to have ready", [
            ("The mission in one sentence.", "Who it serves and what they get. If it takes a paragraph it isn't decided yet."),
            ("Three people", "for a board. One who knows money, one who knows art, one who knows PJ well enough to argue with him."),
            ("A funding rule in writing.", "What share of licensing income goes to the mission, automatically, before anybody debates it."),
        ]),
        quote=("It takes a great deal of time and thought to install work properly.", "Donald Judd &middot; who bought the buildings instead of renting the walls"),
        opens="Mission",
    ),
    dict(
        n=4, year="Circa 2030", title="The Catalogue", express=False, tag="Local only",
        ann=None,
        blocks=[
            ("What this is",
             "Editions closed and stated. This design was fifty, it is gone, here is the proof. Three stores of merch becomes a counted, photographed, categorized inventory. Right now it is stock. After this stop it is a catalogue."),
            ("What to look at",
             "A closed edition is what makes a reissue an event instead of a restock. Same object, completely different value, and the only thing separating them is a number somebody wrote down and stuck to."),
        ],
        now=("Already on this platform",
             "Gumbit is the LeWitt case in physical form. The turnaround drawing is the instruction. The print file is the certificate. "
             "The figure is the execution, and anybody with a printer can run it. What PJ owns, and what has to be numbered, is the file."),
        listy=("What to have ready", [
            ("One row per design.", "Name, year, plate it came from, size of run, how many left."),
            ("Declare each run closed", "in writing, with a date. That declaration is what creates the edition."),
            ("Number what can still be numbered.", "Start with what is on the shelf today."),
        ]),
        quote=("The idea becomes a machine that makes the art.", "Sol LeWitt &middot; 1967 &middot; he sold the instruction, never the wall"),
        opens="Editions",
    ),
    dict(
        n=5, year="Circa 2028", title="The Company", express=False, tag="Local only",
        ann=None,
        blocks=[
            ("What this is",
             "Platform's Edge running at scale. The cart, the cabinet, the booking calendar, ALL CITY shipped, Gumbit produced. Multiple channels, real margins, money coming in that doesn't require PJ to personally stand behind a table every single day."),
            ("What to look at",
             "This is the stop that pays for Stop 3. A foundation with nothing coming in is a piece of paper in a drawer. Haring took real heat for opening a shop and selling his own work cheap, and he was right &mdash; the shop funded everything else and put the work in more hands than any gallery ever did."),
        ],
        listy=("What to have ready", [
            ("Unit cost on every item.", "Blank, ink, labor, shipping. The real number."),
            ("Margin per channel.", "Platform, store, online, event. One of them is quietly losing money and it isn't the obvious one."),
            ("Ninety days logged daily.", "One honest quarter beats three years of memory."),
        ]),
        quote=("Being good in business is the most fascinating kind of art.", "Andy Warhol"),
        opens="Trade",
    ),
    dict(
        n=6, year="Circa 2027", title="The Entity", express=True, tag="Express &middot; Major",
        ann=None,
        blocks=[
            ("What this is",
             "Two companies. One holds the artwork, the trademarks and the copyrights, and PJ owns all of it forever. The other one runs the business, takes the risk, and is the only thing an investor or a landlord ever touches."),
            ("What to look at",
             "If the business has a bad year, the artwork isn't in the room. If the business has a great year, the artwork licenses to it and gets paid. This is the cheapest protective move on the entire line and it is available right now."),
        ],
        now=("In play right now",
             "247 Nostrand Ave and 437 Broadway are both live, and there is a landlord rep agreement on file. "
             "Every one of those is a document somebody signs. The entity wants to exist <em>before</em> the signature, not after &mdash; "
             "a lease signed personally puts the artwork in the room with the risk.<br><br>"
             "And ALL CITY is not one asset. The code, the music, the story bible and the artwork are four separate works, "
             "each one ownable, licensable and assignable on its own. They should be assigned to the holding company by name, not assumed."),
        listy=("What to have ready", [
            ("Search the names first.", "Find out what is available before the signage gets printed, not after."),
            ("File the holding entity", "and formally assign the existing artwork and marks into it, in writing."),
            ("One business bank account.", "Nothing personal running through it, starting day one."),
        ]),
        quote=("Own the name before somebody sells it back to you.", "Not a quotation &mdash; the lesson, plainly"),
        opens="Ownership",
    ),
    dict(
        n=7, year="2026 &middot; You are here", title="The Archive", express=True, tag="Express &middot; Major",
        ann="Now arriving. This stop needs no money, no lawyer, no landlord and nobody's permission. It can start this week.",
        blocks=[
            ("What this is",
             "The pile. Fourteen years of stencils, plates, prints, shirts, photos, receipts, press, and a cease and desist letter from the New York Gaming Commission that nobody has ever written about."),
            ("What to look at",
             "Every stop above this one is built out of this pile. A stencil with a date is evidence. A run with a count is an edition. A story written down is history. Same objects either way &mdash; the only difference is whether somebody wrote it down."),
            (None,
             "And the good news is that the hard part is finished. Fourteen years of making the work is the part most people never do. This is just the part where it gets a name and a number."),
        ],
        now=("Already on this platform",
             "ALL CITY shows what this looks like when it is done properly. Numbered builds going back to v3, a written story bible, "
             "original music, three cut videos &mdash; dated, versioned and kept, nothing saved over. "
             "That is the standard. The stencils and the plates are the part that has never had it."),
        naming=True,
        listy=("Start this week", [
            ("One folder, one naming rule.", "Date first, then name. Boring and permanent beats clever."),
            ("Photograph every plate flat,", "daylight, ruler in the frame for scale. A phone is fine. Consistency matters more than the camera."),
            ("Ten voice memos, ten minutes each.", "Which plate came first, who was there, what the C&amp;D was really about. Nobody else on earth can recover this."),
            ("One box", "for press, receipts, flyers, the letter."),
            ("Count the stock.", "Three stores, one sheet, real numbers."),
        ]),
        quote=("Just DO!", "Sol LeWitt &middot; 1965 &middot; in a letter to a friend who was stuck"),
        opens="The Record",
    ),
    dict(
        n=8, year="Circa 2012", title="The Platform", express=True, tag="Express &middot; Origin",
        ann=None,
        blocks=[
            ("What this is",
             "A homemade cart. A subway platform. Prints for sale to people waiting for a train."),
            ("What to look at",
             "First stop on the line and also the last one, because it is the thing every stop above it sells. The cart is not what PJ did before the real business started. The cart <em>is</em> the real business. Everything after this is the same move at a bigger size."),
        ],
        listy=None,
        quote=("I don't think about art when I'm working. I try to think about life.", "Jean-Michel Basquiat"),
        opens="The Work",
    ),
]

# ---- rides. keyed by the stop they arrive at (page order) ----
RIDES = {
    2: ("Stop 2 to Stop 1", "Let it come back around",
        "The longest ride on the line and there is almost nothing to do on it. The work is made. The record is kept. The market goes away and comes back on its own schedule, and it always comes back. The only job here is to still own the thing when it does."),
    3: ("Stop 3 to Stop 2", "Answer the phone",
        "Once the foundation exists, people start asking. A student writing a thesis. A blog. A small gallery upstate. Say yes to the small ones and keep a file of every ask. That file is what a museum reads before it calls."),
    4: ("Stop 4 to Stop 3", "Decide who it is for",
        "A thinking ride, not a paperwork ride. Say the mission out loud to five different people and watch which version makes them lean in. That is the sentence. Write it down the same day you hear it."),
    5: ("Stop 5 to Stop 4", "Count while you sell",
        "Don't stop selling to build the catalogue. Build it out of the selling. Every time something goes out the door it gets a line: what it was, what run it came from, what is left. Ten seconds a sale, and by the time you pull into Stop 4 the work is already done."),
    6: ("Stop 6 to Stop 5", "Run one channel all the way clean",
        "Not all four at once. Pick the strongest one, get its numbers honest end to end, and use it as the template for the rest. A channel you understand completely beats four you are guessing at."),
    7: ("Stop 7 to Stop 6", "List what is worth keeping",
        "Short ride. While the archive is still fresh, write down every name, mark and design PJ would be angry to lose. That list is exactly what gets filed at Stop 6, and it is far easier to write with the plates still spread out on the table."),
    8: ("Stop 8 to Stop 7", "Keep the cart running",
        "This is the ride PJ has already been on for fourteen years, and it isn't over. Nothing about the archive means stepping off the platform. The cart keeps going out. The difference from here on is that what goes out gets written down on the way."),
}

# ---- service advisories: the warning signs, in MTA poster form ----
ADVISORIES = [
    ("change", "Service change", "Stand clear of the closing doors",
     "A door that shuts on you is a deal signed without reading, a partner with a claim on the work, or a name given away. These do not reopen."),
    ("delay", "Delays", "Step aside and let them off first",
     "Taking on the next thing before the last one has cleared. New channel, new location, new product, while the previous one is still unmeasured."),
    ("work", "Planned work", "Do not lean on the door",
     "Putting weight on something you do not control. A landlord's goodwill, one buyer, one platform's algorithm, one person's handshake."),
    ("watch", "See something, say something", "The problem you spot and do not name",
     "Numbers that do not reconcile. A partner going quiet. An agreement drifting from what was said out loud. Naming it early is the whole trick."),
    ("exp", "Running express", "Trains skip stations",
     "The Express is a real service and sometimes it is the right one. It only hurts when you needed the thing that was sitting at the stop you passed."),
    ("last", "Last stop", "Everyone off",
     "Something that ended. A store, a partnership, a brand name. Worth putting on the record what it was, why it ended and what it cost."),
]


NAMING_BLOCK = """        <div class="naming">
          <span class="lbl">A naming convention</span>
          <p style="margin-top:0">One system, five rules, and it never changes. Every file gets one name, built the same way every time:</p>
          <div class="fmt"><b>2026-09-09</b>_<b>plate</b>_train-king_<b>v01</b>.jpg</div>
          <ol>
            <li><b>Date first, year first.</b> 2026-09-09, never 9/9/26. Written this way the files sort themselves into order forever, in any folder, on any machine.</li>
            <li><b>Then what it is.</b> plate, print, run, press, legal, photo. One word from a short list PJ picks once and never grows.</li>
            <li><b>Then what it's called,</b> in lowercase with hyphens. train-king, not Train King (final)(2).</li>
            <li><b>Then the version, and never overwrite.</b> v01 stays on disk when v02 is made. This is the whole trick and it is the one rule people break. A version you kept is evidence. A version you saved over is gone.</li>
            <li><b>The name carries the facts.</b> If you have to open the file to know what it is, the name failed. Rename it.</li>
          </ol>
          <p>Five rules. No software, no subscription, no app that gets discontinued. It works in a folder on a laptop and it will still work in fifty years, which is the actual requirement.</p>
        </div>
"""


def bands(count, terminating=None):
    """Track column markup: `count` services running, one optionally ending here."""
    out = []
    for k in range(1, count + 1):
        cls = "ln b%d" % k
        if terminating == k:
            cls += " end"
        out.append('<i class="%s" style="background:%s"></i>' % (cls, SERVICES[k - 1]["color"]))
    return "".join(out)


def marker(count, express):
    """Station marker: connector bar across the active services plus a dot on each."""
    out = []
    if count > 1:
        out.append('<i class="bar b%d" style="--span:%d"></i>' % (1, count))
    shape = "x" if express else "o"
    for k in range(1, count + 1):
        out.append('<i class="dot %s b%d"></i>' % (shape, k))
    return '<div class="mk">%s</div>' % "".join(out)


def build():
    w = io.StringIO()
    W = w.write

    # ---------------- CSS ----------------
    css_bands = []
    for k in range(1, 9):
        css_bands.append(".ln.b%d{left:%dpx}" % (k, 8 + (k - 1) * 15))
        css_bands.append(".dot.x.b%d{left:%dpx}" % (k, 4 + (k - 1) * 15))
        css_bands.append(".dot.o.b%d{left:%dpx}" % (k, 7 + (k - 1) * 15))
    css_bands_m = []
    for k in range(1, 9):
        css_bands_m.append(".ln.b%d{left:%dpx}" % (k, 5 + (k - 1) * 9))
        css_bands_m.append(".dot.x.b%d{left:%dpx}" % (k, 1 + (k - 1) * 9))
        css_bands_m.append(".dot.o.b%d{left:%dpx}" % (k, 3 + (k - 1) * 9))

    W("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Line Runs Both Ways</title>
<style>
  :root{
    --ink:#0C0C0C;
    --paper:#F6F2E8;
    --card:#FFFFFF;
    --grey:#78766F;
    --rule:#CFCABB;
    --mta-y:#FCCC0A;
    --mta-r:#EE352E;
    --mta-g:#00933C;
    --mta-b:#0039A6;
  }
  *{box-sizing:border-box}
  html{background:var(--paper)}
  body{
    margin:0;background:var(--paper);color:var(--ink);
    font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;
    font-size:17px;line-height:1.5;-webkit-font-smoothing:antialiased;
  }
  .wrap{max-width:1000px;margin:0 auto;padding:0 28px 120px}
  p{max-width:60ch}

  .cover{padding:72px 0 36px}
  .kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;margin-bottom:26px}
  h1{font-size:64px;line-height:.94;letter-spacing:-.035em;margin:0 0 22px;text-transform:uppercase;font-weight:700}
  .sub{font-size:21px;line-height:1.3;max-width:32ch;margin:0 0 34px}
  .stamp{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--grey);border-top:2px solid var(--ink);padding-top:12px;font-weight:700}

  h2{font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;margin:0 0 16px}
  .rule{border:0;border-top:2px solid var(--ink);margin:60px 0 34px}
  .lede{font-size:32px;line-height:1.04;letter-spacing:-.025em;margin:0 0 16px;text-transform:uppercase;font-weight:700;max-width:22ch}

  .ann{background:var(--ink);color:var(--paper);padding:14px 18px;margin:0 0 22px;max-width:60ch;
       font-size:14px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;line-height:1.45}
  .ann.hold{background:var(--mta-y);color:var(--ink)}

  /* route bullets */
  .bul{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;
       border-radius:50%;color:#fff;font-weight:700;font-size:14px;flex:0 0 26px}
  .bul.dk{color:#0C0C0C}
  .bul.dia{border-radius:2px;transform:rotate(45deg);width:23px;height:23px;flex:0 0 23px}
  .bul.dia span{transform:rotate(-45deg)}

  /* legend */
  .legend{background:var(--card);border:2px solid var(--ink);padding:6px 20px;margin:26px 0 0;max-width:60ch}
  .lrow{display:flex;align-items:flex-start;gap:14px;padding:11px 0}
  .lrow+.lrow{border-top:1px solid var(--rule)}
  .lrow p{margin:0;font-size:15px}
  .lrow b{display:block;text-transform:uppercase;letter-spacing:.06em;font-size:13px}
  .lrow .born{color:var(--grey);font-size:13px;letter-spacing:.06em;text-transform:uppercase;font-weight:700}

  /* ---- the track ---- */
  .row{display:grid;grid-template-columns:132px 1fr}
  .trk{position:relative}
  .ln{position:absolute;top:0;bottom:0;width:9px}
  .ln.end{bottom:auto;height:20px}
  """ + "".join(css_bands) + """
  .mk{position:absolute;top:0;left:0;right:0;height:0;z-index:3}
  .bar{position:absolute;left:12px;top:18px;height:3px;background:var(--ink);
       width:calc((var(--span) - 1) * 15px)}
  .dot{position:absolute;border-radius:50%;background:var(--ink);border:3px solid var(--paper)}
  .dot.x{width:17px;height:17px;top:11px}
  .dot.o{width:11px;height:11px;top:14px}

  .body{padding:0 0 44px;min-height:74px}
  .stophead{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
  .num{font-size:13px;font-weight:700;letter-spacing:.14em}
  .when{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey);font-weight:700}
  .svc{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:3px 8px;color:#fff}
  .svc.e{background:#FF6319}
  .svc.l{background:var(--mta-b)}
  .body h3{font-size:38px;line-height:.98;letter-spacing:-.03em;margin:6px 0 14px;text-transform:uppercase;font-weight:700}
  .opens{display:inline-flex;align-items:center;gap:9px;font-size:12px;letter-spacing:.12em;
         text-transform:uppercase;font-weight:700;color:var(--grey);margin:0 0 14px}
  .body h4{font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;margin:20px 0 5px}
  .body h4+p{margin-top:0}
  .body ul{max-width:60ch;padding-left:20px;margin:5px 0 0}
  .body li{margin-bottom:7px}

  .q{border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);padding:17px 0;margin:22px 0 0;max-width:60ch}
  .q p{font-size:24px;line-height:1.2;letter-spacing:-.02em;margin:0 0 8px;font-weight:700}
  .q .who{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey);font-weight:700}

  .ridecard{background:var(--card);border-left:9px solid var(--mta-y);padding:15px 20px;max-width:60ch}
  .ridecard .lbl{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--grey);display:block;margin-bottom:5px}
  .ridecard h5{font-size:19px;margin:0 0 7px;text-transform:uppercase;letter-spacing:-.01em;font-weight:700}
  .ridecard p{margin:0;font-size:16px}

  /* ---- service advisories ---- */
  .adv{background:var(--card);border:2px solid var(--ink);margin:0 0 16px;max-width:60ch}
  .adv .hd{padding:8px 16px;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase}
  .adv .hd.change{background:var(--mta-y);color:var(--ink)}
  .adv .hd.delay{background:#FF6319;color:#fff}
  .adv .hd.work{background:var(--mta-b);color:#fff}
  .adv .hd.watch{background:var(--ink);color:var(--paper)}
  .adv .hd.exp{background:var(--mta-g);color:#fff}
  .adv .hd.last{background:var(--mta-r);color:#fff}
  .adv .in{padding:14px 16px 16px}
  .adv h5{font-size:21px;margin:0 0 8px;text-transform:uppercase;letter-spacing:-.015em;font-weight:700}
  .adv p{margin:0 0 12px;font-size:16px;max-width:none}
  .slot{border:2px dashed var(--rule);padding:11px 13px;font-size:12px;letter-spacing:.12em;
        text-transform:uppercase;font-weight:700;color:var(--grey)}

  .closer{border-top:9px solid var(--mta-r);padding-top:26px;margin-top:14px}
  .closer .big{font-size:40px;line-height:1;text-transform:uppercase;font-weight:700;letter-spacing:-.03em;max-width:20ch;margin:0 0 18px}
  .closer p{font-size:18px}

  .now{background:var(--card);border-left:9px solid var(--ink);padding:15px 18px;margin:20px 0 0;max-width:60ch}
  .now .lbl{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;display:block;margin-bottom:7px}
  .now p{margin:0 0 10px;font-size:16px;max-width:none}
  .now p:last-child{margin:0}
  .naming{background:var(--ink);color:var(--paper);padding:18px 20px;margin:20px 0 0;max-width:60ch}
  .naming .lbl{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;display:block;margin-bottom:10px;color:var(--mta-y)}
  .naming .fmt{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:15px;line-height:1.9;
               background:rgba(255,255,255,.08);padding:12px 14px;margin:0 0 14px;overflow-x:auto;white-space:nowrap}
  .naming .fmt b{color:var(--mta-y);font-weight:700}
  .naming ol{margin:0;padding-left:20px;max-width:none}
  .naming li{margin-bottom:8px;font-size:15px}
  .naming li b{color:var(--mta-y)}
  .naming p{max-width:none;font-size:15px}

  @media (max-width:700px){
    h1{font-size:40px}
    .lede{font-size:25px}
    .body h3{font-size:27px}
    .closer .big{font-size:28px}
    .q p{font-size:20px}
    .adv h5{font-size:18px}
    .row{grid-template-columns:80px 1fr}
    .ln{width:6px}
    """ + "".join(css_bands_m) + """
    .bar{left:8px;width:calc((var(--span) - 1) * 9px)}
    .dot.x{width:13px;height:13px;top:13px}
    .dot.o{width:9px;height:9px;top:15px}
  }
</style>
</head>
<body>
<div class="wrap">

  <section class="cover">
    <div class="kicker">Platform's Edge &nbsp;/&nbsp; Working document</div>
    <h1>The Line<br>Runs Both<br>Ways</h1>
    <p class="sub">A map of PJ O'Rourke II's career, read from the last stop backwards to the platform he is standing on.</p>
    <div class="stamp">Draft v4 &nbsp;&middot;&nbsp; For PJ &nbsp;&middot;&nbsp; Feldt Design</div>
  </section>

  <section>
    <div class="ann">This is a Reissue-bound train. The next stop is the Archive. Stand clear of the closing doors.</div>
    <h2>How to read this</h2>
    <p class="lede">Start at the end. Work back to where you're standing.</p>
    <p>Most plans run forward and turn into a wish list. This one runs backwards. The last stop is fixed, and every stop above it is there because the one below it makes it possible.</p>
    <p>Watch the left-hand side of the page. At the top, eight coloured services run side by side &mdash; the whole system, working at once. At every stop going down, one of them ends, because that is the year it hadn't started yet. By the bottom of the page there is one track left, and a man with a cart.</p>
    <p>Read down to see where it came from. Read up to see what it becomes.</p>
  </section>

  <section>
    <h2>The services</h2>
""")

    # ---- legend ----
    W('    <div class="legend">\n')
    for s in SERVICES:
        dk = " dk" if s.get("dark") else ""
        W('      <div class="lrow">'
          '<span class="bul%s" style="background:%s">%s</span>'
          '<p><b>%s</b>%s</p>'
          '<span class="born">Begins<br>%s</span>'
          '</div>\n' % (dk, s["color"], s["bullet"], s["name"], s["note"], s["born"]))
    W('    </div>\n')

    W("""
    <div class="legend" style="margin-top:18px">
      <div class="lrow">
        <span class="bul dia" style="background:#FF6319"><span>E</span></span>
        <p><b>Express</b>Five stops. The ones that change what PJ legally owns and what anyone can prove. Big dot on the map.</p>
      </div>
      <div class="lrow">
        <span class="bul" style="background:#0039A6">L</span>
        <p><b>Local</b>All eight. Same track, same terminal, three extra stops where the money and the record get built. Small dot on the map.</p>
      </div>
      <div class="lrow">
        <span class="bul" style="background:#0C0C0C">&bull;</span>
        <p><b>Both trains arrive</b>The Express reaches the Foundation sooner. The Local reaches it with the catalogue counted, the numbers clean and the show already booked. Neither is wrong. Know which one you are on.</p>
      </div>
    </div>
  </section>

  <hr class="rule">

  <section>
    <h2>The line, read backwards</h2>
""")

    # ---- system header: all eight running ----
    W('    <div class="row">\n      <div class="trk">%s</div>\n' % bands(8))
    W('      <div class="body" style="padding-bottom:30px">\n')
    W('        <div class="when">Circa 2075 &middot; the whole system</div>\n')
    W('        <p style="margin:8px 0 0;max-width:52ch">Eight services running at once. Every one of them started somewhere below.</p>\n')
    W('      </div>\n    </div>\n')

    # ---- stops and rides ----
    for stop in STOPS:
        n = stop["n"]
        count = 9 - n          # services still running at this stop
        term = count           # the one that ends here

        # the ride that arrives at this stop (rides sit above their stop, except stop 1)
        if n in RIDES:
            lbl, head, txt = RIDES[n]
            W('    <div class="row">\n      <div class="trk">%s</div>\n' % bands(count))
            W('      <div class="body">\n        <div class="ridecard">\n')
            W('          <span class="lbl">On the train &nbsp;&middot;&nbsp; %s</span>\n' % lbl)
            W('          <h5>%s</h5>\n          <p>%s</p>\n' % (head, txt))
            W('        </div>\n      </div>\n    </div>\n')

        W('    <div class="row">\n      <div class="trk">%s%s</div>\n'
          % (bands(count, terminating=term), marker(count, stop["express"])))
        W('      <div class="body">\n')
        W('        <div class="stophead"><span class="num">STOP %d</span>'
          '<span class="when">%s</span><span class="svc %s">%s</span></div>\n'
          % (n, stop["year"], "e" if stop["express"] else "l", stop["tag"]))
        W('        <h3>%s</h3>\n' % stop["title"])

        svc = SERVICES[term - 1]
        dk = " dk" if svc.get("dark") else ""
        W('        <div class="opens"><span class="bul%s" style="background:%s">%s</span>'
          'Service begins here &mdash; %s</div>\n' % (dk, svc["color"], svc["bullet"], svc["name"]))

        if stop.get("now"):
            nh, nt = stop["now"]
            W('        <div class="now"><span class="lbl">%s</span><p>%s</p></div>\n' % (nh, nt))

        if stop.get("naming"):
            W(NAMING_BLOCK)

        if stop["ann"]:
            W('        <div class="ann hold">%s</div>\n' % stop["ann"])

        for head, txt in stop["blocks"]:
            if head:
                W('        <h4>%s</h4>\n' % head)
            W('        <p>%s</p>\n' % txt)

        if stop["listy"]:
            head, items = stop["listy"]
            W('        <h4>%s</h4>\n        <ul>\n' % head)
            for b, rest in items:
                W('          <li><b>%s</b> %s</li>\n' % (b, rest))
            W('        </ul>\n')

        qt, who = stop["quote"]
        W('        <div class="q"><p>%s</p><div class="who">%s</div></div>\n' % (qt, who))
        W('      </div>\n    </div>\n')

    W("""  </section>

  <hr class="rule">

  <section>
    <h2>Service advisories</h2>
    <p class="lede">Six things that take the line out.</p>
    <p style="margin-bottom:26px">Every one of these has happened to somebody. Most have happened to PJ. The signs are written; the stories underneath them go in after the interview.</p>
""")
    for cls, kind, head, txt in ADVISORIES:
        W('    <div class="adv">\n      <div class="hd %s">%s</div>\n      <div class="in">\n' % (cls, kind))
        W('        <h5>%s</h5>\n        <p>%s</p>\n' % (head, txt))
        W('        <div class="slot">To be filled after the interview</div>\n')
        W('      </div>\n    </div>\n')

    W("""  </section>

  <hr class="rule">

  <section class="closer">
    <h2>Why backwards</h2>
    <p class="big">Everything old is new more than once.</p>
    <p>Haring got called a graffiti kid, then got canonized, then got written off as too commercial, and now hangs in museums that would not have let him in the door in 1982. Four turns of the same wheel around one body of work, and the work never changed once.</p>
    <p>The market leaves and the market comes back. That is not a risk, it is a schedule. The only thing that decides whether PJ is there when it comes back around is whether he still has the work, still owns it, and can still prove it is his.</p>
    <p style="margin-top:24px;font-weight:700">Eight services at the top of this page. One track at the bottom. All of it is the cart.</p>
    <div class="ann" style="margin-top:28px">This is the last stop on this train. Everybody stays on.</div>
  </section>

</div>
</body>
</html>
""")
    return w.getvalue()


if __name__ == "__main__":
    out = build()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote %d bytes to %s" % (len(out), OUT))
