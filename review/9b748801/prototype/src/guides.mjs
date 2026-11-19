// Guides. Each block is one of: ["p", text] | ["h2", text] | ["ul", [items]] | ["q", question-answer-pair-free text]
// Claims about products use only values recorded in data/products.json (title-as-listed).
// Working titles are hypotheses, not claims about popularity, search volume or product quality.

export const guides = [
  {
    slug: "basket-or-oven-air-fryer",
    title: "Basket or oven-style air fryer: what should you compare?",
    description: "A plain checklist for choosing between a basket air fryer and an oven-style air fryer, using only what the listings state.",
    date: "2026-11-19",
    category: "air-fryers",
    summary: "Two shapes, two sets of trade-offs. What each listing actually tells you, and what it doesn't.",
    body: [
      ["p", "Most of the air fryers we track come in two shapes. A basket model uses a drawer you pull out and shake. An oven-style model is a countertop box with a door, racks, and often a second heating zone. The shape changes almost everything else, so compare the shape first."],
      ["h2", "Questions to ask before you compare brands"],
      ["ul", [
        "How many people usually eat from one batch? A single basket fills faster than a multi-rack oven.",
        "Do you bake, roast or toast as well as fry? Oven-style models list more functions; check which ones the listing names.",
        "Where will it sit? Measure the counter depth and height yourself, because the listings in this study did not confirm dimensions.",
        "Will you clean it by hand or in the dishwasher? Check the listing for dishwasher-safe parts before you assume it."
      ]],
      ["h2", "What the listings in this study state"],
      ["p", "Our listing records (see the Products table) show a 6 Quart dual-basket model, an 8 Qt model whose title lists a 4-in-1 function set and one basket, and a 26 QT oven-style model with 24 one-touch presets. Those numbers come from the product titles. They are the only capacity figures we treat as verified."],
      ["h2", "What this guide does not tell you"],
      ["p", "It does not say which shape is better. It does not compare prices, ratings or reviews, because those were not confirmed for each product. Read the product's own listing before you buy, and use the Verification page to see exactly what was checked."]
    ]
  },
  {
    slug: "air-fryer-capacity-checklist",
    title: "A no-hype checklist for comparing air fryer capacity",
    description: "How to compare air fryer capacity without relying on marketing numbers, with the capacity values as listed in each product title.",
    date: "2026-11-19",
    category: "air-fryers",
    summary: "Quarts, baskets and presets are not the same thing. Here is how to read them.",
    body: [
      ["p", "Capacity is one of the first numbers a listing shows, and one of the easiest to misread. A quart figure can describe the whole unit, a single basket, or an interior volume. Before you compare two models, find out which of those the listing means."],
      ["h2", "A four-step check"],
      ["ul", [
        "Read the capacity in the title. Write it down exactly as printed (for example, '6 Quart' or '26QT').",
        "Check whether the listing says 'per basket' or 'total'. Check whether the number applies to the whole unit or to each basket.",
        "Count how many people you cook for and how many batches you want per meal.",
        "Check the product details table for dimensions before you decide, because capacity does not tell you footprint."
      ]],
      ["h2", "Capacity values in this study"],
      ["ul", [
        "CHEFMAN 6 Quart Dual Basket model: '6 Quart' and '2 Independent 3Qt' baskets (title).",
        "Chefman 8 Qt TurboFry model: '8 Qt' (title).",
        "Emeril Lagasse 26QT French Door model: '26QT' with '24 One-Touch Preset Options' (title)."
      ]],
      ["h2", "What we did not do"],
      ["p", "We did not convert quarts to litres or calculate usable food volume, because the listings did not confirm a usable-volume figure. We also did not rank the models. Ranking would need tested results, which this site does not have."]
    ]
  },
  {
    slug: "cleanup-and-counter-space",
    title: "How to assess cleanup and counter-space trade-offs",
    description: "A practical way to weigh cleanup effort and counter space for kitchen appliances, using the listing details that are actually confirmed.",
    date: "2026-11-19",
    category: "air-fryers",
    summary: "The cheapest appliance can be the most expensive to live with. Here is how to weigh cleanup and space.",
    body: [
      ["p", "Two things decide whether an appliance stays on the counter or in the cupboard: how long cleaning takes, and how much space it takes up. Neither shows up clearly in a headline capacity figure."],
      ["h2", "Cleanup questions"],
      ["ul", [
        "Are the baskets, trays and racks listed as dishwasher-safe? Check the title and the product details.",
        "How many removable parts does the model have? Count them from the product photos on the listing, not from memory.",
        "Is there a nonstick coating, and does the listing describe its material? Record exactly what it says."
      ]],
      ["h2", "Counter-space questions"],
      ["ul", [
        "Measure the spot you have: width, depth and clearance above the unit, including the space to open a door or pull a drawer.",
        "Compare that with the dimensions in the product details table. This site did not confirm dimensions for the five products, so it does not publish a figure.",
        "Ask whether you need the space for the appliance all the time, or only on the days you use it."
      ]],
      ["h2", "A worksheet"],
      ["p", "Write down three numbers for each candidate: its listed capacity, its listed dimensions, and the number of parts you would wash. Put them side by side. The trade-off usually shows up in that table, not in the headline."],
      ["h2", "Limits of this guide"],
      ["p", "This guide does not calculate capacity per centimetre of counter depth. That calculation needs confirmed dimensions, which are still missing (see Open questions Q-06)."]
    ]
  },
  {
    slug: "multi-function-appliance-questions",
    title: "Questions to ask before buying a multi-function kitchen appliance",
    description: "Questions to ask before buying a multi-function kitchen appliance, so the function list answers what you actually cook.",
    date: "2026-11-19",
    category: "air-fryers",
    summary: "A long function list is only useful if it matches what you cook. Here is how to check.",
    body: [
      ["p", "Multi-function appliances advertise long lists of functions. A function list is useful only if you cook the things on it. Start with your week, not with the box."],
      ["h2", "Questions to ask"],
      ["ul", [
        "Which three things do I cook most often? Write them down before you open any listing.",
        "Does the listing name the functions I need, in its title or product details?",
        "What temperature range does the listing state? Check the maximum, not only the marketing claim.",
        "Does a function I would use need an accessory that is not included?",
        "How long does a typical cycle take, and does the listing state a time? If it does not, say so in your notes."
      ]],
      ["h2", "How the listings in this study compare on function claims"],
      ["p", "The Emeril Lagasse 26QT listing states '24 One-Touch Preset Options' and 'Six Cooking Accessories Included' in its title. The Chefman 8 Qt listing states '4-in-1' and a '450°F Hi-Fry option' in its title. Those are the only function claims we record as verified."],
      ["h2", "What this guide cannot tell you"],
      ["p", "It cannot tell you whether a function works well. Testing is not part of this site. Use the listing and any reviews you read as evidence, and note how many reviews support each claim."]
    ]
  },
  {
    slug: "meat-thermometer-listing-checklist",
    title: "What should you check on a meat thermometer listing before you buy?",
    description: "What to check on a meat thermometer listing before buying: accuracy, probes, range and connectivity, using only title-level details.",
    date: "2026-11-19",
    category: "meat-thermometers",
    summary: "Accuracy, response time, probes and wireless range. The listing usually states them; here is where to look.",
    body: [
      ["p", "Meat thermometers are sold on speed, accuracy and convenience. Those three claims are easy to state and hard to check. Start with what the listing prints in plain words."],
      ["h2", "Checklist"],
      ["ul", [
        "Accuracy: is a number given, and is it stated as a tolerance (for example ±0.5℉)? Note the exact wording.",
        "Response time: is a time given (for example '1 Sec')? A time claim without a test condition is only a claim.",
        "Probes: how many, and are they ultra-thin or standard? Count them on the listing.",
        "Wireless: if the model is wireless, check the stated range and whether it needs an app.",
        "Heat resistance and waterproofing: note the stated maximum temperature and the stated IP rating."
      ]],
      ["h2", "What the listings in this study state"],
      ["ul", [
        "ThermoMaven 1 Sec: '±0.5℉ Accuracy', 'NIST&NSF Certified', '1 Sec' and 'IP67 Waterproof' (title).",
        "CHEF iQ Sense Gen3: '3 Ultra-Thin Probes', 'WiFi Unlimited Range', '1000°F Heat Safe' and '5 Sensors' (title)."
      ]],
      ["h2", "What this guide does not do"],
      ["p", "It does not test accuracy, and it does not compare prices or ratings, which were not confirmed for these products. Certification wording is quoted from the listing title and should be checked against the certifying body before you rely on it."]
    ]
  }
];
