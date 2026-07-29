
QUESTION_URL = "https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question"
QUESTIONS_URL = "https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-questions"

TOPICS={
        "Math": [
            "Algebra",
            "Advanced Math",
            "Problem-Solving and Data Analysis",
            "Geometry & Trigonometry"
        ],
        "English": [
            "Craft and Structure",
            "Information and Ideas",
            "Standard English Conventions",
            "Expression of Ideas"
        ]
    }
SUB_TOPICS={
    "Algebra": [
        "Linear equations in one variable",
        "Linear functions",
        "Linear equations in two variables",
        "Systems of two linear equations in two variables",
        "Linear inequalities in one or two variables"
    ],

    "Advanced Math": [
        "Nonlinear functions",
        "Nonlinear equations in one variable and systems of equations in two variables",
        "Equivalent expressions"
    ],

    "Problem-Solving and Data Analysis": [
        "Ratios, rates, proportional relationships, and units",
        "Percentages",
        "One-variable data: distributions and measures of center and spread",
        "Two-variable data: models and scatterplots",
        "Probability and conditional probability",
        "Inference from sample statistics and margin of error",
        "Evaluating statistical claims: observational studies and experiments"
    ],

    "Geometry & Trigonometry": [
        "Area and volume",
        "Lines, angles, and triangles",
        "Right triangles and trigonometry",
        "Circles"
    ],

    "Information and Ideas": [
        "Central Ideas and Details",
        "Inferences",
        "Command of Evidence"
    ],

    "Craft and Structure": [
        "Words in Context",
        "Text Structure and Purpose",
        "Cross-Text Connections"
    ],

    "Expression of Ideas": [
        "Rhetorical Synthesis",
        "Transitions"
    ],

    "Standard English Conventions": [
        "Boundaries",
        "Form, Structure, and Sense"
    ]
}

SUB_TOPIC_TIME = {
    "Linear equations in one variable": 60,
    "Linear functions": 75,
    "Linear equations in two variables": 75,
    "Systems of two linear equations in two variables": 90,
    "Linear inequalities in one or two variables": 75,

    "Nonlinear functions": 90,
    "Nonlinear equations in one variable and systems of equations in two variables": 105,
    "Equivalent expressions": 75,

    "Ratios, rates, proportional relationships, and units": 75,
    "Percentages": 60,
    "One-variable data: distributions and measures of center and spread": 75,
    "Two-variable data: models and scatterplots": 90,
    "Probability and conditional probability": 90,
    "Inference from sample statistics and margin of error": 105,
    "Evaluating statistical claims: observational studies and experiments": 90,

    "Area and volume": 90,
    "Lines, angles, and triangles": 75,
    "Right triangles and trigonometry": 90,
    "Circles": 90,

    "Central Ideas and Details": 75,
    "Inferences": 75,
    "Command of Evidence": 95,

    "Words in Context": 45,
    "Text Structure and Purpose": 75,
    "Cross-Text Connections": 80,

    "Rhetorical Synthesis": 80,
    "Transitions": 40,

    "Boundaries": 40,
    "Form, Structure, and Sense": 55
}

DIFFICULTY={
    "Easy":"E",
    "Medium":"M",
    "Hard":"H"
}

