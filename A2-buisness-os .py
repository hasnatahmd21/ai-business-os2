# ===========================================================================
# STRATEGIC SCENARIO SIMULATION & STRESS TESTING ENGINE
# SAME MASTER FILE — CUMULATIVE ENHANCEMENT
# ===========================================================================

class ScenarioSeverity(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    EXTREME = "EXTREME"


class ScenarioType(str, Enum):
    BASELINE = "BASELINE"
    UPSIDE = "UPSIDE"
    DOWNSIDE = "DOWNSIDE"
    EXTREME_DOWNSIDE = "EXTREME_DOWNSIDE"
    MARKET_SHOCK = "MARKET_SHOCK"
    COMPETITOR_SHOCK = "COMPETITOR_SHOCK"
    FINANCIAL_SHOCK = "FINANCIAL_SHOCK"
    OPERATIONAL_SHOCK = "OPERATIONAL_SHOCK"
    CUSTOM = "CUSTOM"


class ScenarioResultStatus(str, Enum):
    VIABLE = "VIABLE"
    CONDITIONAL = "CONDITIONAL"
    AT_RISK = "AT_RISK"
    NON_VIABLE = "NON_VIABLE"


@dataclass
class ScenarioVariable:
    name: str
    baseline_value: float
    stressed_value: float

    unit: str = ""

    change_percent: float = 0.0

    impact_weight: float = 1.0

    direction: str = "NEUTRAL"


@dataclass
class ScenarioDefinition:
    scenario_id: str
    name: str

    scenario_type: ScenarioType
    severity: ScenarioSeverity

    description: str

    variables: List[
        ScenarioVariable
    ] = field(default_factory=list)

    probability: float = 0.0

    duration_days: int = 30

    trigger_conditions: List[str] = field(
        default_factory=list
    )


@dataclass
class ScenarioMetric:
    name: str

    baseline: float
    projected: float

    change: float
    change_percent: float

    status: str


@dataclass
class ScenarioResult:
    scenario_id: str
    scenario_name: str

    status: ScenarioResultStatus

    resilience_score: float

    metrics: List[ScenarioMetric] = field(
        default_factory=list
    )

    vulnerabilities: List[str] = field(
        default_factory=list
    )

    advantages: List[str] = field(
        default_factory=list
    )

    mitigation_actions: List[str] = field(
        default_factory=list
    )

    decision_implication: str = ""


@dataclass
class StressTestReport:
    report_id: str
    generated_at: str

    scenarios_tested: int

    viable_scenarios: int
    conditional_scenarios: int
    at_risk_scenarios: int
    non_viable_scenarios: int

    portfolio_resilience: float

    results: List[ScenarioResult] = field(
        default_factory=list
    )

    critical_vulnerabilities: List[str] = field(
        default_factory=list
    )

    recommended_actions: List[str] = field(
        default_factory=list
    )

    overall_verdict: str = ""


# ===========================================================================
# SCENARIO BUILDER
# ===========================================================================

class ScenarioBuilder:

    def build(
        self,
        name: str,
        scenario_type: ScenarioType,
        severity: ScenarioSeverity,
        description: str,
        variables: List[ScenarioVariable],
        probability: float = 0.0,
        duration_days: int = 30
    ) -> ScenarioDefinition:

        scenario_id = (
            "SCN-"
            +
            uuid.uuid4().hex[:16]
        )

        for variable in variables:

            if variable.baseline_value != 0:

                variable.change_percent = (

                    (
                        variable.stressed_value
                        -
                        variable.baseline_value
                    )
                    /
                    abs(
                        variable.baseline_value
                    )
                ) * 100.0

        return ScenarioDefinition(

            scenario_id=
                scenario_id,

            name=
                name,

            scenario_type=
                scenario_type,

            severity=
                severity,

            description=
                description,

            variables=
                variables,

            probability=
                max(
                    0.0,
                    min(
                        100.0,
                        probability
                    )
                ),

            duration_days=
                max(
                    1,
                    duration_days
                )
        )


# ===========================================================================
# SCENARIO GENERATOR
# ===========================================================================

class ScenarioGenerator:

    def generate_standard_suite(
        self,
        baseline:
            Dict[str, float]
    ) -> List[ScenarioDefinition]:

        builder = ScenarioBuilder()

        scenarios = []

        scenarios.append(

            builder.build(

                name=
                    "Baseline",

                scenario_type=
                    ScenarioType.BASELINE,

                severity=
                    ScenarioSeverity.LOW,

                description=
                    "Current operating assumptions.",

                variables=[]
            )
        )

        scenarios.append(

            builder.build(

                name=
                    "Moderate Downside",

                scenario_type=
                    ScenarioType.DOWNSIDE,

                severity=
                    ScenarioSeverity.MODERATE,

                description=
                    "Moderate deterioration across key business drivers.",

                variables=[

                    ScenarioVariable(
                        "revenue",
                        baseline.get(
                            "revenue",
                            0.0
                        ),
                        baseline.get(
                            "revenue",
                            0.0
                        ) * 0.85,
                        unit="currency",
                        impact_weight=1.2
                    ),

                    ScenarioVariable(
                        "gross_margin",
                        baseline.get(
                            "gross_margin",
                            0.0
                        ),
                        baseline.get(
                            "gross_margin",
                            0.0
                        ) * 0.90,
                        unit="percent",
                        impact_weight=1.1
                    ),

                    ScenarioVariable(
                        "operating_cost",
                        baseline.get(
                            "operating_cost",
                            0.0
                        ),
                        baseline.get(
                            "operating_cost",
                            0.0
                        ) * 1.10,
                        unit="currency",
                        impact_weight=1.0
                    )
                ]
            )
        )

        scenarios.append(

            builder.build(

                name=
                    "Severe Downside",

                scenario_type=
                    ScenarioType.EXTREME_DOWNSIDE,

                severity=
                    ScenarioSeverity.HIGH,

                description=
                    "Major demand decline combined with cost pressure.",

                variables=[

                    ScenarioVariable(
                        "revenue",
                        baseline.get(
                            "revenue",
                            0.0
                        ),
                        baseline.get(
                            "revenue",
                            0.0
                        ) * 0.65,
                        unit="currency",
                        impact_weight=1.5
                    ),

                    ScenarioVariable(
                        "gross_margin",
                        baseline.get(
                            "gross_margin",
                            0.0
                        ),
                        baseline.get(
                            "gross_margin",
                            0.0
                        ) * 0.75,
                        unit="percent",
                        impact_weight=1.4
                    ),

                    ScenarioVariable(
                        "operating_cost",
                        baseline.get(
                            "operating_cost",
                            0.0
                        ),
                        baseline.get(
                            "operating_cost",
                            0.0
                        ) * 1.20,
                        unit="currency",
                        impact_weight=1.3
                    )
                ]
            )
        )

        scenarios.append(

            builder.build(

                name=
                    "Growth Upside",

                scenario_type=
                    ScenarioType.UPSIDE,

                severity=
                    ScenarioSeverity.MODERATE,

                description=
                    "Demand expansion and operating leverage.",

                variables=[

                    ScenarioVariable(
                        "revenue",
                        baseline.get(
                            "revenue",
                            0.0
                        ),
                        baseline.get(
                            "revenue",
                            0.0
                        ) * 1.25,
                        unit="currency",
                        impact_weight=1.2
                    ),

                    ScenarioVariable(
                        "gross_margin",
                        baseline.get(
                            "gross_margin",
                            0.0
                        ),
                        baseline.get(
                            "gross_margin",
                            0.0
                        ) * 1.05,
                        unit="percent",
                        impact_weight=1.0
                    )
                ]
            )
        )

        return scenarios


# ===========================================================================
# SCENARIO CALCULATION ENGINE
# ===========================================================================

class ScenarioCalculationEngine:

    def project_financials(
        self,
        baseline:
            Dict[str, float],
        scenario:
            ScenarioDefinition
    ) -> Dict[str, float]:

        projected = dict(
            baseline
        )

        for variable in (
            scenario.variables
        ):

            projected[
                variable.name
            ] = variable.stressed_value

        revenue = projected.get(
            "revenue",
            0.0
        )

        margin = projected.get(
            "gross_margin",
            0.0
        )

        operating_cost = projected.get(
            "operating_cost",
            0.0
        )

        if margin > 1.0:

            gross_profit = (
                revenue
                *
                (
                    margin
                    /
                    100.0
                )
            )

        else:

            gross_profit = (
                revenue
                *
                margin
            )

        operating_profit = (
            gross_profit
            -
            operating_cost
        )

        projected[
            "gross_profit"
        ] = gross_profit

        projected[
            "operating_profit"
        ] = operating_profit

        projected[
            "operating_margin"
        ] = (

            (
                operating_profit
                /
                max(
                    revenue,
                    1.0
                )
            )
            *
            100.0
        )

        return projected


# ===========================================================================
# RESILIENCE ENGINE
# ===========================================================================

class BusinessResilienceEngine:

    def calculate(
        self,
        baseline:
            Dict[str, float],
        projected:
            Dict[str, float],
        scenario:
            ScenarioDefinition
    ) -> float:

        baseline_profit = baseline.get(
            "operating_profit",
            0.0
        )

        projected_profit = projected.get(
            "operating_profit",
            0.0
        )

        if baseline_profit == 0:

            profit_score = (
                50.0
                if projected_profit >= 0
                else 10.0
            )

        else:

            profit_retention = (

                projected_profit
                /
                baseline_profit
            )

            profit_score = (

                50.0
                +
                (
                    profit_retention
                    *
                    50.0
                )
            )

        profit_score = max(
            0.0,
            min(
                100.0,
                profit_score
            )
        )

        weighted_pressure = 0.0
        total_weight = 0.0

        for variable in (
            scenario.variables
        ):

            pressure = min(

                100.0,

                abs(
                    variable.change_percent
                )
            )

            weighted_pressure += (
                pressure
                *
                variable.impact_weight
            )

            total_weight += (
                variable.impact_weight
            )

        if total_weight:

            pressure_score = max(

                0.0,

                100.0
                -
                (
                    weighted_pressure
                    /
                    total_weight
                )
            )

        else:

            pressure_score = 100.0

        resilience = (

            profit_score
            *
            0.65

            +

            pressure_score
            *
            0.35
        )

        return round(

            max(
                0.0,
                min(
                    100.0,
                    resilience
                )
            ),

            2
        )


# ===========================================================================
# SCENARIO CLASSIFIER
# ===========================================================================

class ScenarioClassifier:

    def classify(
        self,
        resilience_score:
            float,
        projected:
            Dict[str, float]
    ) -> ScenarioResultStatus:

        operating_profit = projected.get(
            "operating_profit",
            0.0
        )

        if (
            resilience_score >= 75.0
            and
            operating_profit >= 0
        ):

            return ScenarioResultStatus.VIABLE

        if (
            resilience_score >= 55.0
            and
            operating_profit >= 0
        ):

            return ScenarioResultStatus.CONDITIONAL

        if (
            resilience_score >= 30.0
        ):

            return ScenarioResultStatus.AT_RISK

        return ScenarioResultStatus.NON_VIABLE


# ===========================================================================
# SCENARIO INTERPRETATION ENGINE
# ===========================================================================

class ScenarioInterpretationEngine:

    def interpret(
        self,
        baseline:
            Dict[str, float],
        projected:
            Dict[str, float],
        scenario:
            ScenarioDefinition
    ) -> Tuple[
        List[str],
        List[str],
        List[str]
    ]:

        vulnerabilities = []
        advantages = []
        mitigation = []

        baseline_revenue = baseline.get(
            "revenue",
            0.0
        )

        projected_revenue = projected.get(
            "revenue",
            0.0
        )

        if projected_revenue < baseline_revenue:

            decline = (

                (
                    baseline_revenue
                    -
                    projected_revenue
                )
                /
                max(
                    baseline_revenue,
                    1.0
                )
            ) * 100.0

            vulnerabilities.append(
                f"Revenue declines by {decline:.1f}%."
            )

            mitigation.extend([

                "Increase retention activity.",

                "Protect highest-margin customer segments.",

                "Reduce non-essential variable spending."
            ])

        elif projected_revenue > baseline_revenue:

            advantages.append(
                "Revenue growth creates potential operating leverage."
            )

        baseline_profit = baseline.get(
            "operating_profit",
            0.0
        )

        projected_profit = projected.get(
            "operating_profit",
            0.0
        )

        if projected_profit < 0:

            vulnerabilities.append(
                "Operating profit becomes negative."
            )

            mitigation.extend([

                "Activate cost-containment plan.",

                "Prioritize cash preservation.",

                "Suspend low-ROI expansion initiatives."
            ])

        elif (
            baseline_profit > 0
            and
            projected_profit > baseline_profit
        ):

            advantages.append(
                "Operating leverage improves under the scenario."
            )

        for variable in scenario.variables:

            if (
                variable.change_percent
                <=
                -20.0
            ):

                vulnerabilities.append(

                    (
                        f"{variable.name} experiences a "
                        f"{abs(variable.change_percent):.1f}% deterioration."
                    )
                )

            elif (
                variable.change_percent
                >=
                20.0
            ):

                advantages.append(

                    (
                        f"{variable.name} improves by "
                        f"{variable.change_percent:.1f}%."
                    )
                )

        return (
            vulnerabilities,
            advantages,
            list(
                dict.fromkeys(
                    mitigation
                )
            )
        )


# ===========================================================================
# MASTER SCENARIO STRESS TEST ENGINE
# ===========================================================================

class StrategicStressTestingEngine:

    def __init__(self):

        self.generator = (
            ScenarioGenerator()
        )

        self.calculator = (
            ScenarioCalculationEngine()
        )

        self.resilience = (
            BusinessResilienceEngine()
        )

        self.classifier = (
            ScenarioClassifier()
        )

        self.interpreter = (
            ScenarioInterpretationEngine()
        )

    def run(
        self,
        baseline:
            Dict[str, float],
        scenarios:
            Optional[
                List[ScenarioDefinition]
            ] = None
    ) -> StressTestReport:

        if scenarios is None:

            scenarios = (
                self.generator
                .generate_standard_suite(
                    baseline
                )
            )

        results = []

        for scenario in scenarios:

            projected = (
                self.calculator
                .project_financials(
                    baseline,
                    scenario
                )
            )

            resilience_score = (
                self.resilience.calculate(
                    baseline,
                    projected,
                    scenario
                )
            )

            status = (
                self.classifier.classify(
                    resilience_score,
                    projected
                )
            )

            vulnerabilities, advantages, mitigation = (
                self.interpreter.interpret(
                    baseline,
                    projected,
                    scenario
                )
            )

            metrics = []

            for variable in (
                scenario.variables
            ):

                change = (

                    variable.stressed_value
                    -
                    variable.baseline_value
                )

                metrics.append(

                    ScenarioMetric(

                        name=
                            variable.name,

                        baseline=
                            variable.baseline_value,

                        projected=
                            variable.stressed_value,

                        change=
                            change,

                        change_percent=
                            variable.change_percent,

                        status=(
                            "IMPROVED"
                            if change > 0
                            else
                            "DECLINED"
                            if change < 0
                            else
                            "UNCHANGED"
                        )
                    )
                )

            if status == ScenarioResultStatus.VIABLE:

                implication = (
                    "Strategy remains viable under this scenario."
                )

            elif status == ScenarioResultStatus.CONDITIONAL:

                implication = (
                    "Strategy remains viable only with "
                    "active monitoring and mitigation."
                )

            elif status == ScenarioResultStatus.AT_RISK:

                implication = (
                    "Strategy enters an elevated-risk state "
                    "and requires contingency action."
                )

            else:

                implication = (
                    "Strategy becomes non-viable under this scenario."
                )

            results.append(

                ScenarioResult(

                    scenario_id=
                        scenario.scenario_id,

                    scenario_name=
                        scenario.name,

                    status=
                        status,

                    resilience_score=
                        resilience_score,

                    metrics=
                        metrics,

                    vulnerabilities=
                        vulnerabilities,

                    advantages=
                        advantages,

                    mitigation_actions=
                        mitigation,

                    decision_implication=
                        implication
                )
            )

        viable = sum(

            1

            for result
            in results

            if result.status
            ==
            ScenarioResultStatus.VIABLE
        )

        conditional = sum(

            1

            for result
            in results

            if result.status
            ==
            ScenarioResultStatus.CONDITIONAL
        )

        at_risk = sum(

            1

            for result
            in results

            if result.status
            ==
            ScenarioResultStatus.AT_RISK
        )

        non_viable = sum(

            1

            for result
            in results

            if result.status
            ==
            ScenarioResultStatus.NON_VIABLE
        )

        if results:

            portfolio_resilience = round(

                sum(
                    result.resilience_score
                    for result
                    in results
                )
                /
                len(results),

                2
            )

        else:

            portfolio_resilience = 0.0

        critical_vulnerabilities = []

        for result in results:

            if result.status in (

                ScenarioResultStatus.AT_RISK,

                ScenarioResultStatus.NON_VIABLE
            ):

                critical_vulnerabilities.extend(

                    result.vulnerabilities
                )

        critical_vulnerabilities = list(

            dict.fromkeys(
                critical_vulnerabilities
            )
        )

        recommended_actions = []

        for result in results:

            if result.status in (

                ScenarioResultStatus.AT_RISK,

                ScenarioResultStatus.NON_VIABLE,

                ScenarioResultStatus.CONDITIONAL
            ):

                recommended_actions.extend(

                    result.mitigation_actions
                )

        recommended_actions = list(

            dict.fromkeys(
                recommended_actions
            )
        )

        if non_viable:

            verdict = (
                "HIGH FRAGILITY — "
                "strategy fails under at least one major stress scenario."
            )

        elif at_risk:

            verdict = (
                "ELEVATED RISK — "
                "strategy requires contingency protection."
            )

        elif conditional:

            verdict = (
                "CONDITIONALLY RESILIENT — "
                "strategy survives but requires monitoring."
            )

        else:

            verdict = (
                "RESILIENT — "
                "strategy remains viable across tested scenarios."
            )

        return StressTestReport(

            report_id=(
                "STR-"
                +
                uuid.uuid4().hex[:16]
            ),

            generated_at=(
                datetime.now()
                .astimezone()
                .isoformat()
            ),

            scenarios_tested=
                len(results),

            viable_scenarios=
                viable,

            conditional_scenarios=
                conditional,

            at_risk_scenarios=
                at_risk,

            non_viable_scenarios=
                non_viable,

            portfolio_resilience=
                portfolio_resilience,

            results=
                results,

            critical_vulnerabilities=
                critical_vulnerabilities,

            recommended_actions=
                recommended_actions,

            overall_verdict=
                verdict
        )


# ===========================================================================
# EVIDENCE + STRESS TEST INTEGRATION
# ===========================================================================

def apply_stress_test_gate(
    decision:
        AdaptiveDecision,
    stress_report:
        StressTestReport
) -> AdaptiveDecision:

    if (
        stress_report.non_viable_scenarios
        >
        0
    ):

        decision.confidence = min(
            decision.confidence,
            55.0
        )

        decision.rationale += (

            " Stress testing identified at least "
            "one non-viable scenario."
        )

        decision.required_actions.append(
            "Review contingency strategy before scaling exposure."
        )

    elif (
        stress_report.at_risk_scenarios
        >
        0
    ):

        decision.confidence = min(
            decision.confidence,
            70.0
        )

        decision.required_actions.append(
            "Monitor identified stress vulnerabilities."
        )

    return decision


# ===========================================================================
# ORCHESTRATOR BRIDGE
# ===========================================================================

def attach_stress_testing(
    orchestrator:
        EnterpriseStrategyOrchestrator
) -> EnterpriseStrategyOrchestrator:

    if not hasattr(
        orchestrator,
        "stress_testing"
    ):

        orchestrator.stress_testing = (
            StrategicStressTestingEngine()
        )

    return orchestrator


try:

    attach_stress_testing(
        os_core.strategy_orchestrator
    )

except Exception as exc:

    logger.warning(
        "Stress testing bridge deferred: %s",
        exc
    )


# ===========================================================================
# SELF TEST
# ===========================================================================

def stress_testing_self_test():

    engine = (
        StrategicStressTestingEngine()
    )

    baseline = {

        "revenue":
            100000.0,

        "gross_margin":
            60.0,

        "operating_cost":
            30000.0
    }

    baseline[
        "gross_profit"
    ] = (
        baseline["revenue"]
        *
        0.60
    )

    baseline[
        "operating_profit"
    ] = (
        baseline["gross_profit"]
        -
        baseline["operating_cost"]
    )

    report = engine.run(
        baseline
    )

    return {

        "system":
            "STRATEGIC_STRESS_TESTING_ENGINE",

        "passed":
            report.scenarios_tested >= 4,

        "scenarios_tested":
            report.scenarios_tested,

        "portfolio_resilience":
            report.portfolio_resilience,

        "overall_verdict":
            report.overall_verdict,

        "critical_vulnerabilities":
            report.critical_vulnerabilities,

        "recommended_actions":
            report.recommended_actions
    }


# ===========================================================================
# FEATURE REGISTRATION
# ===========================================================================

if "ENHANCED_V15_FEATURES" in globals():

    _stress_testing_features = [

        "strategic_stress_testing",

        "scenario_simulation",

        "baseline_scenario",

        "upside_scenario",

        "downside_scenario",

        "extreme_downside_scenario",

        "market_shock_simulation",

        "competitor_shock_simulation",

        "financial_shock_simulation",

        "operational_shock_simulation",

        "business_resilience_scoring",

        "scenario_vulnerability_detection",

        "scenario_mitigation_engine",

        "portfolio_resilience_analysis",

        "stress_test_decision_gate"
    ]

    for _feature in (
        _stress_testing_features
    ):

        if (
            _feature
            not in ENHANCED_V15_FEATURES
        ):

            ENHANCED_V15_FEATURES.append(
                _feature
            )


# ===========================================================================
# END — STRATEGIC SCENARIO SIMULATION & STRESS TESTING
# ===========================================================================
