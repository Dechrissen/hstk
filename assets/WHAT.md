# What are "Headline Snaps"?

Headline Snaps are part of an experiment a friend and I started some time during our college years.

Essentially, they are **fabricated news headlines** inspired mostly by real world events, but exaggerated for comedic effect. Specifically, the source data we're working with is `.png` or `.jpeg` files, created via Snapchat, with a plain black background and white text as the news headline.

<p align="center"><img src="../assets/example_headline.jpg" alt="example headline snap" style="width:30%"/></p>

Once we realized the comedy and entertainment they could provide, we started sending each other Headline Snaps more frequently, to the point where we've now amassed several thousand of them over the course of 6-7 years. The sheer volume led us to want to convert them into some form of analyzable data, so we could run various experiments (graphs, trends, language models, text synthesis). This is what sparked the motivation for this project.

I preferred to keep this project a set of tools (hence 'toolkit'), rather than "pre-made database plus specific set of experiments" created from our current set of source data. This way, it can be applied to future sets of Headline Snaps, should anyone decide to emulate this experiment with friends of their own. I think it's interesting to see the interplay between two (or more) participants' unique experiences and sense of humor, once the source material is converted to useable data throughout the pipeline created in this project. From there, it can be used to generate new Headline Snaps in a way that captures a **fusion of the sentiments of the contributions to the dataset**.

Of course, the particular incarnation of the data (an image file with text representation) is not optimal (neither for ease of creation nor data processing). But, for us, it became such a habit, and our existing thousands of Headline Snaps were in this form already. So I decided that part of the pipeline for data processing would need to be an OCR step, since black background + white text is rather ideal for OCRing. It became an element of the learning aspect of this project.

### Learning outcomes

- more Python
- OCR/Tesseract
- Image processing via PIL
- argparse
- language models / text synthesis
- sqlite
- data analysis via word clouds, etc.
