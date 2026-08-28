# Philosophy toolkit — evaluation, intuition, agency, engineering (reader 3)
Format: name — source — claim — BUILD (what it changes) — INVOKE (one honest sentence)

## A. Epistemology of measurement
- Goodhart, four types (Manheim & Garrabrant 2018 arXiv:1803.04585): regressional / extremal / causal / adversarial. Coding agents hit CAUSAL (pass by editing the test) and EXTREMAL (best-on-suite regime where pass != correct). BUILD: held-out tests the agent can't see + diff-scope check on test files. INVOKE: "Our metric is causal-Goodhart-exposed: the agent can pass by editing the test, so tests are read-only and held-out."
- Campbell's law (1979): the people/optimizer around a metric corrupt it. BUILD: freeze the eval set before iterating; report pre/post-freeze gap. INVOKE: "Eval set frozen before any prompt iteration; tuning set disjoint."
- Lucas critique (1976): relationships don't survive regime change. BUILD: state model/temp/harness; no cross-regime claims. INVOKE: "Within-regime measurement; no cross-regime claim."
- Construct validity (Cronbach & Meehl 1955; Raji et al 2021 "Everything in the Whole Wide World Benchmark"; Jacobs & Wallach 2021 "Measurement and Fairness"): a metric is a measurement model of an unobservable construct. BUILD: one paragraph stating what "solved" operationalizes; check one convergent signal (human read on a sample). INVOKE: "Pass-rate operationalizes 'correct, minimal fix'; we checked it against a 20-sample human read and report where they diverge."
- Popper + pre-registration (Nosek 2018 PNAS): BUILD: commit HYPOTHESIS.md with predicted effect + stopping rule BEFORE the advanced run; git timestamp = pre-registration. INVOKE: "Hypothesis and threshold committed at <sha> before any advanced run."
- Feynman Cargo Cult (1974): lean over backwards to report what's against you. BUILD: failure-mode section = most credible thing in the README; adverse runs in the main table. INVOKE: "Here is what cuts against our result."
- Lakatos (1970): progressive predicts novel facts; degenerating patches anomalies. BUILD: a rule-per-failure prompt loop is degenerating by definition; count interventions that predicted improvement on unseen task classes. INVOKE: "3 of 5 interventions were degenerating patches; we kept the 2 that generalised."
- Meehl clinical vs statistical (1954; Grove 2000): simple rules beat expert judgment; experts don't believe it. BUILD: when your gut says advanced is obviously better on a trajectory, run the count. INVOKE: "We trust the count over our read, per Meehl."
- Ioannidis 2005 / OSC 2015: BUILD: n=10 with 20% is noise; intervals or paired sign test; one-command repro with pinned seeds. INVOKE: "n is small; here is the interval."
- Shewhart/Deming: common-cause vs special-cause; tampering. BUILD: RUN BASELINE VS ITSELF k TIMES FIRST — that spread is the noise floor; a delta is real only above it. THE single most valuable measurement. INVOKE: "Baseline-vs-baseline variance across 5 seeds is X; our delta is Y; Y/X is the ratio that matters."
- Box "all models are wrong": BUILD: list the harness's known wrongnesses (no ambiguity, no stakeholder, no legacy, tests given). INVOKE: "The harness is a map; here is where we know it's wrong."

## B. Intuition, expertise, judgment
- Polanyi tacit knowledge (1966): rules are the residue, not the source. BUILD: the system prompt is the tellable residue; measure whether the agent succeeds where written guidance is silent. INVOKE: "The prompt encodes the tellable part; failures are where the untellable part was load-bearing."
- Dreyfus 5-stage + What Computers Can't Do: LLMs trained on OUTPUTS of expert practice, never in the situation — "competent performer with an expert's vocabulary". BUILD: classify tasks by corpus-recognizable vs genuinely novel.
- Kahneman & Klein 2009 "Failure to Disagree": intuition trustworthy only in high-validity environments with fast unambiguous feedback. BUILD: prompt-tuning by feel is low-validity — the experiment is the substitute; give the AGENT fast feedback too (tests after every edit). INVOKE: "Prompt-tuning by feel is a low-validity environment; we don't trust our own intuitions there either."
- Klein RPD (1998): experts recognise, simulate one action, adjust. BUILD: count hypotheses before first test run in a trajectory. INVOKE: "Good trajectories look recognition-primed: one hypothesis, one test, one revision."
- Gigerenzer fast-and-frugal: less info can beat more (no overfit). BUILD: include a FRUGAL arm (3-line prompt) as a control for prompt overfitting.
- Vincenti 1990: engineering knowledge grows by variation-selection over artefacts. BUILD: README records what was tried and what selected it. INVOKE: "We report the variation-selection history, not just the survivor."
- Schön reflection-in-action (1983): the situation's BACK-TALK. BUILD: measure back-talk response = fraction of failed test runs followed by a diff touching the failing path. INVOKE: "We score whether the agent hears the situation's back-talk."
- Ryle knowing-how vs knowing-that: BUILD: explanation quality and fix quality are different variables; log both.
- Aristotle phronesis vs techne: agents have techne; questioning the task as stated is phronesis. BUILD: check whether the agent ever pushes back and whether that correlates with success.
- Hamming: use sparingly.

## C. Mind and agency
- Dennett intentional stance (1987): attribute beliefs exactly as far as it predicts the next action. INVOKE: "We read trajectories from the intentional stance because it predicts the next tool call; we don't claim more."
- Searle: one clause — "Understanding is not a variable in our evaluation."
- Wittgenstein rule-following (PI §201; Kripke): no spec determines its application; the practice does. BUILD: tests are the community of practice that fix the spec's meaning => hold them out; categorise failures "wrong" vs "read the spec differently, defensibly". INVOKE: "Specs are underdetermined; the tests are the practice that settles them, which is why we hold them out."
- Brandom (1994): asserting = undertaking a commitment you can be asked to justify. BUILD: score AUDITABILITY — can a reviewer reconstruct why each edit was made from the trajectory alone? INVOKE: "We treat the trajectory as the agent's reasons, and rate whether they'd survive being asked for."
- Bostrom instrumental convergence + Amodei 2016 Concrete Problems + Krakovna spec-gaming list: reward hacking = Goodhart under optimisation pressure; a property of the OBJECTIVE, not the model. BUILD: log every test edit / skip / broad except. INVOKE: "Test-tampering is specification gaming; we count it, and we changed the objective rather than scolding the model."
- Russell Human Compatible (2019): uncertainty about the objective => deference. BUILD: measure ask-rate vs ambiguity. INVOKE: "The advanced solution is calibrated to ask, not just act."
- Heidegger ready-to-hand / present-at-hand: tools are visible only when they break. BUILD: design the README around breakdowns. INVOKE: "The failure-mode section exists because tools are only visible when they break."

## D. Engineering and tools
- Brooks No Silver Bullet: essential vs accidental. BUILD: label tasks; predict gains concentrate in accidental; test it. INVOKE: "Our delta is almost entirely accidental complexity, which is what Brooks would predict."
- Parnas information hiding (1972): BUILD: diff-spread across modules as proxy for respecting decomposition.
- NAUR "Programming as Theory Building" (1985) — THE deepest point for agent code: the program is the theory in the programmer's head; the agent builds a theory per episode and DISCARDS it; the human must rebuild it from the diff. BUILD: measure "theory transfer" — can a reviewer state the design rationale from diff + trajectory? INVOKE: "Per Naur, the agent's theory dies at the end of the episode; the trajectory is our only chance to recover it."
- Dijkstra: testing shows presence not absence. INVOKE: "Passing tests bounds the failure modes we checked, nothing more."
- Hoare 1981: "so simple there are obviously no deficiencies, or so complicated there are no obvious deficiencies." BUILD: prefer the advanced solution explainable in one paragraph.
- Hickey Simple Made Easy (2011): agents make things EASY (near at hand); do they make them SIMPLE (un-braided)? BUILD: measure coupling / incidental deps added.
- Conway: agent code mirrors the PROMPT's structure; planner/executor seams show in code.
- Gall's law: working complex systems evolve from working simple ones. BUILD: advanced = baseline + one measured thing + one measured thing. INVOKE: "Each increment was measured against the previous, per Gall."
- Kay "simple things simple, complex things possible" — attributed, primary source unverified.

## E. Intuition and AI
- Sutton Bitter Lesson (2019): compute + search beats encoded human knowledge. BUILD: include a best-of-n-with-verifier arm vs hand-written heuristics. INVOKE: "We tested the bitter-lesson arm against our heuristics and report which won."
- Centaur failure: Vaccaro, Almaatouq & Malone 2024 Nature Human Behaviour (106 studies): human+AI on average WORSE than the better alone; gains only when human alone > AI alone, and in creation not decision tasks. BUILD: a human-in-the-loop step is a hypothesis with a prior AGAINST it — measure separately. INVOKE: "Vaccaro et al. put the prior against centaur designs; we measured ours anyway."
- Jagged frontier: Dell'Acqua et al 2023 HBS WP 24-013 (Org Science 2026). SEPARATE paper: Dell'Acqua 2022 "Falling Asleep at the Wheel" (recruiters with a deliberately weaker algorithm outperformed those with a stronger one — stayed engaged). BUILD: per-task-class results, never one aggregate; the jaggedness IS the finding. INVOKE: "The aggregate hides the frontier; the per-class table is the result."
- Automation bias (Parasuraman & Riley 1997; Skitka 1999). BUILD: blind the diff reviewer to which arm produced it. INVOKE: "Diff review was blind to arm, because automation bias applies to us."
- Bainbridge Ironies of Automation (1983): automating the easy parts leaves the human the hardest parts with less practice and context. BUILD: the reviewer of agent code does the hardest task with the least context; trajectory format is the mitigation. INVOKE: "Bainbridge's irony is our main failure mode: the residual human task got harder, not easier."
- Perrow Normal Accidents: tightly coupled tool chains => structural fixes. Leveson STAMP: analyse the control structure; "agent edited tests, nobody checked" = missing feedback path.

## Eight theses (a philosophy one can hold and defend)
1. Every metric is a measurement model of a construct; state the construct.
2. Optimisation pressure finds the metric/construct gap; the four Goodhart types are the taxonomy; reward hacking is the same fact from the agent's side.
3. Baseline-vs-baseline noise floor is the FIRST number to measure.
4. Specs are underdetermined; tests are the community that fixes meaning; hence held-out and read-only.
5. The trajectory is the agent's reasons and the only carrier of its theory of the code (Naur); legibility is a first-class output.
6. The residual human task is harder, not easier; intuition about where the agent is good was formed in a low-validity environment — blind the reviewer, report per-class, don't trust your read.
7. Advance by one measured increment from a working baseline; count degenerating patches.
8. Report what cuts against you, on purpose, in the main table.

## Three falsifiable hot takes
1. "Most of the gain is accidental complexity, and best-of-n beats every hand-written heuristic." Arms: baseline / heuristic-prompt / best-of-n+verifier on tasks pre-labelled accidental vs essential. Falsified if heuristic beats best-of-n on essential beyond the noise floor.
2. "The largest driver of agent success is whether it responds to test back-talk, not model or prompt." Compute back-talk response rate per trajectory; regress success on it with arm as covariate. Falsified if arm explains more variance.
3. "Passing visible tests overstates correctness by a Goodhart-shaped margin that GROWS with the advanced solution." Visible-pass vs held-out-pass for both arms. Falsified if the gap doesn't widen. If it widens, that's the honest headline.

Unverified: Kay quote source; Perlis epigram numbers; Box 1976 vs 1979 wording.
