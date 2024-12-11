# %% Cell 1
import yaflux as yf


class Analysis(yf.Base):
    """Example analysis with multiple dependency paths."""

    @yf.step(creates="a")
    def step_a(self) -> int:
        return 42

    @yf.step(creates="b", requires="a")
    def step_b(self) -> int:
        return 42

    @yf.step(creates=["c", "d"], requires=["a", "b"])
    def step_c(self) -> tuple[int, int]:
        return (42, 42)

    @yf.step(creates="e", requires="c")
    def step_d(self) -> int:
        return 42

    @yf.step(creates="f", requires="d")
    def step_e(self) -> int:
        return 42

    @yf.step(creates="sub_a", requires="c")
    def branch_a(self) -> int:
        return 42

    @yf.step(creates="sub_b", requires="d")
    def branch_b(self) -> int:
        return 42

    @yf.step(creates="g", requires=["e", "f"])
    def final(self) -> int:
        return 42
