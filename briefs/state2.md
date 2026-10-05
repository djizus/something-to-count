# Brief: the narrative state, rebuilt chapter by chapter

A long story drifts in three ways: facts change between chapters, people act on knowledge they do not have yet, and things are planted and never paid. A short, typed record that is updated after every chapter catches all three. The record in `state.md` is out of date: it was built from an earlier text with one chapter fewer. Rebuild it from the book as it stands, and use the rebuilding to find every continuity error.

The book is `manuscript/00.md` to `17.md`. Open nothing else but this brief. The old `state.md` is not to be read.

## The procedure

Work through the chapters **in order, one at a time**. Do not read ahead. For each chapter:

1. **Check it against the state so far.** Before you change the state, compare the chapter with it. Note every place where the chapter disagrees with what the state holds: a fact, a number, a date or a clock time, a day of the week, where a person is, what a person knows and when they learned it, what a person has on them, which hand, which side, the weather, the level of the river, the wording of something quoted or written down, how a thing in the world works. Quote the sentence in this chapter and give the state entry it disagrees with, with its chapter.
2. **Then update the state once**, with four kinds of change and no others:
   - **overwrite a person's snapshot** in full, for each person the chapter changed. A snapshot is not a history. It holds where they are, what they want now, who they stand how with, what they know (with the chapter where they learned it), what they have on them or in their keeping, and their bodily and emotional condition. There is one snapshot per person per village: the two villages have their own Coralie, Larrère, Jeannot, Maïté, Kévin, Sarthou, Madame Etcheto and so on, and the two women each have a list of what they have received from the other.
   - **add a fixed fact**: something the chapter has set that a later chapter could get wrong. One line, with a short key and the chapter. Numbers, dates, the river's level on each date in each village, what the weather did each day, who telephoned whom and when, exact words quoted or written down, what a room contains, how the crossing between the villages has been seen to work.
   - **add something owed**: an object shown, a question asked, a promise, a threat, a running line with a pay-off due. One line, with a key and the chapter where it was planted.
   - **resolve something owed**: delete the entry when a chapter pays it, and note the chapter in a short "paid" list.

Keep a calendar as you go: for each village, each date from 23 November to 15 December 2026 that the book touches, with the day of the week, the weather, the river, and who was in whose body. The book also fixes a night in 2014. Check every day of the week against its date (1 December 2026 is a Tuesday).

## Write `state.md`

Overwrite the file. Five parts, every entry with a short key in backticks:

1. **People**, as they stand at the end of chapter 17.
2. **Fixed by the text.**
3. **Calendar**, as a table for each village.
4. **Owed**: what is still unpaid at the end of the book, and after it the list of what was paid and where. For each thing still unpaid, say whether the book plainly means to leave it open.
5. **Contradictions**: everything step 1 found, in chapter order, sorted as fact, timeline, knowledge, object or body, world, or wording. For each: both sentences quoted, both chapters, and the smallest change that would mend it, saying which of the two places should change. Do not list a thing that only looks odd. List a thing only if two places in the book cannot both be true, or a person acts on something they cannot know yet.

## Rules

- Parts 1 to 4 together stay under 3,500 words. Part 5 is as long as it needs to be.
- Do not edit the manuscript.
- Nothing you write mentions any writing tool, model, vendor or session. Do not run git.

Reply in four lines: how many contradictions of each kind, the three worst, how many things are still owed, and the word count of the state.
