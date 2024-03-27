> I like to think (and
> the sooner the better!)
> of a cybernetic meadow
> where mammals and computers
> live together in mutually
> programming harmony
> like pure water
> touching clear sky. 

\- [Richard Brautigan](https://allpoetry.com/All-Watched-Over-By-Machines-Of-Loving-Grace)

## Meadow

Meadow is a personal AI copilot for deep work. The very first version is a _head's up display for active reading_. Think [JARVIS](https://en.wikipedia.org/wiki/J.A.R.V.I.S.) but studying and reflecting.

## The first use case

The first use case is as a thread-following assistant for when I'm sitting at my desk reading. As I read I encounter a million little threads I could follow. Some of these threads I note with a physical mark in the book. Some of the threads are urgent enough that I follow them immediately. Most of the time, following a thread has a high cost, the cost of falling out of or failing to enter a flowstate.

Some threads are never followed. In fact, if I really pay attention I notice that the _vast majority of threads are never followed_. As we read we maintain a mental "image" of whatever we're reading. The fidelity and resolution of that image are both imperfect. Every tiny discrepancy between the source text and our mental image could be considered a thread. One example which is salient to my life right now is geographical context. Imagine if all the relevant maps were always just a glance away regardless of the book you were reading. Imagine if for every dialogue there was a _dramatis personae_ just a hotkey away. More generally:

_What if we had a system that reads along with us, notices all the little threads, and anticipates what additional context we might want?  What if that system could also research and/or generate the context we need? If we never had to follow these threads ourselves, how much deeper could we sink into our learning environment?_

## A broader vision

Ultimately I want to be able to do serious, productive thinking without sitting at my desk. I want to be able to go for a hike and write a technical proposal for a new software system, I want to be able to decode some opaque scholastic apologia while riding a bike, I want to be able to learn to speak Arabic while walking down the beach, etc.

Further down the road, I want Meadow to go with me everywhere. But I specifically want Meadow to follow me around at home. Today we have "Alexa, is it going to rain today?" but I want "Meadow, how much will it cost to fix this sprinkler?" or "Meadow, where did I put the multi-tool?". I want Meadow to help keep me in a flow state, to help manage the inifinite threads of _life_ rather than just the ones I find in books.

## Meadow v0.0.1

We're building a _Head's Up Display for Active Reading_. Here's the logical architecture:

![Logical Architecture](./assets/meadow-architecture.png)

The first version is basic. In words it's as follows:

- The user has a _window_ into some _source material_. The window represents the specific part of the source material which is most likely to be active right now inside the user's head.
- The window is fed as input into Meadow. The window could be physically any number of things. It could be an open PDF, or a web browser, or a video feed of an open book, etc.

- In _passive_ mode, Meadow parses the feed for likely open _threads_. A thread is a path leading away from the source material which the user may want to follow. 
- In _active mode_, Meadow additionally parses some kind of user input. Each user input indicates to Meadow which specific thread to follow. For example, if the user highlights a paragraph and draws a "?" next to it, Meadow can assume that the user doesn't understand the meaning of the paragraph.
- Meadow follows the thread through various reference tools and generates _contexts_ which the user may find interesting.
- Meadow outputs these context's into the _head's up display_. The head's up display could be physically a browser window, or a text log, or audio out, etc.

For Meadow v0.0.1 we need to make some decisions about which specific implementation we should use for each of the above components. A first pass at the decisions:

- The quickest version for source material could be an ordered list of markdown files. The window could be a single file. I think I'm going to jump over this step and go straight to a video feed of an open book. It's not strictly the best decision from an operational POV, but I want to do it because
  1. I personally want to use Meadow when I read phyiscal books,
  2. Multimodal AI is kinda hot right now so there's a lot of activity to draw on, and
  3. It just seems way cooler for Meadow to "see".
- Passive mode only.
- I'm reading through a 4000-page history of philosophy, so the threads I want are:
  - a bio of each historical figure
  - a map of each geographical location
  - a translation of all non-English text
- I've been using GPT-4 "manually" via ChatGPT as I've been reading recently, and it does a remarkable job of answering my questions, so I'm just going to worry about GPT-4 as a reference for now.
- The head's up display will just be a text file that I can `tail -f`.

# Development Roadmap

1. Given a page in a book, "parse" the image.

Off the top of my head there's a few ways we could do this:

- Use an OCR library like [tesseract](https://github.com/tesseract-ocr/tesseract)
- Use a multimodal LLM
- Use a third-party OCR (e.g. [google cloud vision](https://cloud.google.com/vision/docs/ocr), [AWS textract](https://aws.amazon.com/textract/), or [Azure document intelligence]).

I think we're going to try to use `tesseract` then if that doesn't work one of the hosted APIs. If quality is still not great maybe there's an opportunity to use a multimodal LLM to improve the quality.

Actually, now that I think about it, maybe the whole magic of multimodal LLMs is that I don't have to parse the image. I can just pass an image of the page with a prompt that like, say, "Please give me a list of all the historical figures on this page.".

I'm still going to try the LLM-first approach last because I'm pretty confident that I'm going to want to compute things from the raw text. If I never parse the image then I'm going to be constantly bottlenecked by the multimodality, I think.

Update:

Tesseract seems to be the most popular open source OCR tool and it doesn't work very well at all for my use case. It seems like Tesseract is very picky about the quality of the image along certain dimensions and can work very well if you make sure to control for all those dimensions. So maybe I could get it to work well for a single picture, but it seems highly unlikely that I'll get it to work well with _live video of the book I'm reading_.

So I think I'm going to move onto trying out one of the hosted APIs. I'm not super hopeful about these, but we'll see. It's interesting because I've kind of been thinking that the actual LLM agent core of this project was small enough that it might already be a solved-ish problem and that I'm reinventing the wheel. But now it looks like I'm going to have to implement an agent just to get a decent feed of the book, which is great because it's evidence I have a real problem. Also, I found [this library](https://github.com/mercoa-finance/llm-document-ocr) which might help.


Update 2024-03-27-00

So the AWS Textract API actually seems to work quite well, way better than `tesseract` and it also includes bounding boxes for the text it finds.

If I were to take a snapshot of the page every 3 seconds for 3 hours, that would be a little less than $6.00 in API costs. It would somewhere around $150/month, which isn't that crazy as a starting point. Of course, that's super inefficient. What we could do is use a local LLM to detect page turns, or something like that. I wonder how well a small LLM could answer "What page is the reader looking at right now?"

Update 2024-03-32-01

I spent about an hour building a rig to suspend a webcam over the book I'm reading. It looks like my webcam can't support this application, its resolution is too low. I don't know anything about cameras, but I think "resolution" is the correct term. If I put the camera far enough away from the book that the whole book is in view, then the letters are super fuzzy. I briefly considered by a new webcam or digital camera, I don't think I need a very nice one, just something better than my $25 USB camera. Then I remember Amber already has a digital camera. But then I found about the new [continuity camera](https://support.apple.com/en-us/102546) that lets you use your iphone or ipad as a webcam. So that's the next step:

_Use the continuity camera API to capture video from a python script._

There's also this feature called "desktop view" which uses software to simulate a top-down view of your desk. That could be _perfect_ if it works well enough to resolve the printed characters!!!