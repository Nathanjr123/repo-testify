.PHONY: setup baseline advanced eval ablate report test proof traces video-check sanity
PY=python3
setup:
	@$(PY) -c "import sys; assert sys.version_info>=(3,10)" && echo "python ok"
sanity:
	$(PY) -m eval.runner --arm baseline --cases eval/cases/public --sanity
baseline:
	$(PY) -m eval.runner --arm baseline --cases eval/cases/public
advanced:
	$(PY) -m eval.runner --arm advanced --cases eval/cases/public
eval:
	$(PY) -m eval.runner --arm baseline --cases eval/cases/heldout
	$(PY) -m eval.runner --arm advanced --cases eval/cases/heldout
ablate:
	@for f in $$( $(PY) -c "import json;print(' '.join(json.load(open('arms/advanced/flags.json'))))" ); do \
	  ADVANCED_DISABLE=$$f $(PY) -m eval.runner --arm advanced --cases eval/cases/public --label ablate-$$f ; done
report:
	$(PY) -m eval.report > RESULTS.md && head -40 RESULTS.md
replay:
	$(PY) -m eval.replay --run $(RUN)
traces:
	$(PY) tools/export_traces.py
test:
	$(PY) -m eval.selftest && $(PY) eval/validate_cases.py
video-check:
	@test -f video.mp4 && test $$(stat -c%s video.mp4) -gt 500000 && ffprobe -v error -show_entries format=duration video.mp4 || echo "video.mp4 missing/too small"
