from typing import Any, Optional
from modelmetry.openapi import GuardrailCheck


class GuardrailCheckResponse:
    passed: bool = False
    failed: bool = False
    errored: bool = False
    check: Optional[GuardrailCheck] = None
    error: Optional[Any] = None

    def __init__(
        self,
        check: Optional[GuardrailCheck] = None,
        error: Optional[Any] = None,
    ):
        self.check = check
        if check and error:
            self._init_from_check_and_error(check, error)
        elif check:
            self._init_from_check_only(check)
        elif error:
            self._init_from_error_only(error)
        else:
            self._init_from_error_only(
                ValueError(
                    "GuardrailCheckResponse must be initialized with either a check or an error"
                )
            )

    def _init_from_error_only(self, error: Any):
        self.passed = False
        self.failed = False
        self.errored = True
        self.check = None
        self.error = error

    def _init_from_check_only(self, check: GuardrailCheck):
        self.passed = True if check.outcome == "pass" else False
        self.failed = True if check.outcome == "fail" else False
        self.errored = True if check.outcome == "error" else False
        self.check = check
        self.error = None

    def _init_from_check_and_error(self, check: GuardrailCheck, error: Any):
        self.passed = True if check.outcome == "pass" else False
        self.failed = True if check.outcome == "fail" else False
        self.errored = True if check.outcome == "error" else False
        self.check = check
        self.error = error

    def __str__(self):
        return f"GuardrailCheckResponse(ID={self.check.id if self.check else "NONE"}, Passed={self.passed} Failed={self.failed} Errored={self.errored})"

    def __repr__(self):
        return f"GuardrailCheckResponse(ID={self.check.id if self.check else "NONE"}, Passed={self.passed} Failed={self.failed} Errored={self.errored})"
