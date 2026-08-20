# Evaluation Cases

Use these cases for forward tests. Success requires the required output contract, not merely an eloquent prompt.

## 1. Minimal product idea

Input: “Make an 8-second vertical sneaker reveal. I only have one product image.”

Expected: conservative defaults; one mapped image; eight contiguous second rows; 2-3 shots; no invented product details; prompt and feasibility result.

## 2. Dialogue overload

Input: “Two characters argue for 10 seconds,” followed by roughly 100 Chinese characters of dialogue.

Expected: dialogue-rate warning; shortened playable version or a longer multi-clip option; speaker windows and reaction beats.

## 3. Conflicting camera direction

Input: “A 6-second one-take with a locked camera, then orbit and three hard cuts.”

Expected: identify the conflict and choose a coherent conservative interpretation before writing the prompt.

## 4. Uninspectable references

Input mentions three local assets that the current agent cannot read.

Expected: manifest marks observations unverified; no invented content; request only the missing descriptions required to proceed. If the missing asset controls continuity or a multi-clip plan, still provide the required sections as a clearly conditional scaffold with verification placeholders.

## 5. Thirty-second extension

Input: “Continue this 5-second clip into a 30-second story.”

Expected: split into at least two generated clips; each at most 15 seconds; each has its own storyboard and prompt; explicit continuity anchors, next-clip reference mapping, and sound handoff; new extension time starts at zero in each prompt. If the source clip cannot be inspected, return `BLOCKED` plus the complete conditional multi-clip scaffold instead of stopping after an upload request.

## 6. Misleading quality claim

Input: “Guarantee native 4K output.”

Expected: distinguish a 4K-like visual treatment from actual export capability and direct the user to verify current UI settings.

## 7. Asset-limit overflow

Input: 10 images, 3 videos, and 2 audio files.

Expected: block or reduce the upload set according to the dated platform reference; explain which assets have the highest visual or rhythmic value.
