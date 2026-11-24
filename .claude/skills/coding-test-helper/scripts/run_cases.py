"""
코딩테스트 풀이를 직접 고른 테스트 케이스로 돌려 보는 도구.

케이스마다 별도 프로세스에서 제한 시간을 두고 실행하므로, 무한 루프가 있어도 멈추지 않는다.

사용법
------
1) 프로그래머스 (solution 함수):
   python3 run_cases.py func <solution.py> <cases.json> [--timeout 2]

   cases.json 예:
   [
     {"name": "예제1", "args": [[1,2,3,4,5], 7], "expected": [2,3]},
     {"name": "최대 입력", "args_expr": "[[1]*999999+[1000], 1000]", "expected": [999999, 999999]}
   ]
   - args      : solution(*args)로 넘길 인자 목록
   - args_expr : 큰 입력은 파이썬 식으로 (예: "[[3]*300000, [1]*300000]")
   - expected  : 생략하면 결과만 출력
   - check     : 정답이 여러 개일 수 있으면 파이썬 식으로 판정 (변수: result, args). 예: "abs(sum(result)) == 1"

2) 백준 (표준 입력/출력):
   python3 run_cases.py stdin <solution.py> <cases.json> [--timeout 2]

   cases.json 예:
   [
     {"name": "예제", "input": "5\\n-2 4 -99 -1 98\\n", "expected": "-99 98"},
     {"name": "최대 입력", "input_expr": "'100000\\\\n' + ' '.join(map(str, range(1, 100001))) + '\\\\n'"}
   ]
   - 출력 비교는 앞뒤 공백을 무시하고 줄 단위로 한다.
   - check 식의 변수: output(문자열), input(문자열)

주의: 백준 템플릿은 같은 폴더의 input.txt를 우선 읽는다.
      이 도구로 돌릴 때는 환경변수 RUN_CASES=1 을 넘기므로, 템플릿이 그 경우 input.txt를 건너뛰게 할 수 있다.
"""
import argparse
import json
import os
import subprocess
import sys
import time

FUNC_RUNNER = r"""
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("sol", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
args = json.loads(sys.stdin.read())
res = mod.solution(*args)
print(json.dumps(res, ensure_ascii=False))
"""


def build_args(case):
    if "args_expr" in case:
        return eval(case["args_expr"])
    return case.get("args", [])


def build_input(case):
    if "input_expr" in case:
        return eval(case["input_expr"])
    return case.get("input", "")


def short(text, limit=60):
    text = str(text).replace("\n", " ⏎ ")
    return text if len(text) <= limit else text[:limit] + " …"


def run_func(sol, case, timeout):
    args = build_args(case)
    start = time.time()
    try:
        p = subprocess.run(
            [sys.executable, "-c", FUNC_RUNNER, sol],
            input=json.dumps(args), capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return args, None, f"{timeout}초 초과 (무한 루프/시간 초과 의심)", timeout
    elapsed = time.time() - start
    if p.returncode != 0:
        err = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else "알 수 없는 에러"
        return args, None, f"에러: {err}", elapsed
    out_lines = p.stdout.strip().splitlines()
    result = json.loads(out_lines[-1]) if out_lines else None
    note = "print 출력 있음 (제출 전 삭제)" if len(out_lines) > 1 else ""
    return args, result, note, elapsed


def run_stdin(sol, case, timeout):
    data = build_input(case)
    env = dict(os.environ, RUN_CASES="1")
    start = time.time()
    try:
        p = subprocess.run(
            [sys.executable, sol], input=data, capture_output=True, text=True,
            timeout=timeout, env=env, cwd=os.path.dirname(os.path.abspath(sol)) or ".",
        )
    except subprocess.TimeoutExpired:
        return data, None, f"{timeout}초 초과 (무한 루프/시간 초과 의심)", timeout
    elapsed = time.time() - start
    if p.returncode != 0:
        err = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else "알 수 없는 에러"
        return data, None, f"에러: {err}", elapsed
    return data, p.stdout, "", elapsed


def safe_check(expr, scope, note):
    """정답이 여러 개일 수 있는 케이스 판정. 결과 형식이 틀려 식이 에러나면 오답으로 처리한다."""
    try:
        return bool(eval(expr, scope)), note
    except Exception as e:
        return False, (note + " " if note else "") + f"판정 실패: {type(e).__name__}"


def normalize(text):
    return [line.strip() for line in str(text).strip().splitlines()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["func", "stdin"])
    ap.add_argument("solution")
    ap.add_argument("cases")
    ap.add_argument("--timeout", type=float, default=2.0)
    a = ap.parse_args()

    with open(a.cases, encoding="utf-8") as f:
        cases = json.load(f)

    passed = 0
    print("| # | 케이스 | 입력 | 결과 | 정답 | 시간 |")
    print("|---|---|---|---|---|---|")
    for i, case in enumerate(cases, 1):
        name = case.get("name", f"case{i}")
        if a.mode == "func":
            given, result, note, t = run_func(a.solution, case, a.timeout)
            shown_in = case.get("args_expr") or json.dumps(given, ensure_ascii=False)
            shown_out = note if result is None else json.dumps(result, ensure_ascii=False)
            if result is None:
                ok = False
            elif "check" in case:
                ok, note = safe_check(case["check"], {"result": result, "args": given}, note)
            elif "expected" in case:
                ok = result == case["expected"]
            else:
                ok = None
        else:
            given, output, note, t = run_stdin(a.solution, case, a.timeout)
            shown_in = case.get("input_expr") or given
            shown_out = note if output is None else output.strip()
            if output is None:
                ok = False
            elif "check" in case:
                ok, note = safe_check(case["check"], {"output": output, "input": given}, note)
            elif "expected" in case:
                ok = normalize(output) == normalize(case["expected"])
            else:
                ok = None

        mark = "" if ok is None else (" ✅" if ok else " ❌")
        if ok:
            passed += 1
        if note and result_is_present(a.mode, locals()):
            shown_out += f" ({note})"
        expected = case.get("expected", case.get("check", "-"))
        print(f"| {i} | {name} | `{short(shown_in)}` | `{short(shown_out)}`{mark} | `{short(json.dumps(expected, ensure_ascii=False) if not isinstance(expected, str) else expected)}` | {t:.2f}s |")

    graded = sum(1 for c in cases if "expected" in c or "check" in c)
    print(f"\n통과 {passed} / 채점 {graded} (전체 {len(cases)})")


def result_is_present(mode, scope):
    return (scope.get("result") is not None) if mode == "func" else (scope.get("output") is not None)


if __name__ == "__main__":
    main()
