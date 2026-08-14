QUESTION_URL="https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question"
QUESTIONS_URL="https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-questions"


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


MATH_SUB_TOPICS={
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
        "One-variable data: Distributions and measures of center and spread",
        "Two-variable data: Models and scatterplots",
        "Probability and conditional probability",
        "Inference from sample statistics and margin of error",
        "Evaluating statistical claims: Observational studies and experiments"
    ],

    "Geometry & Trigonometry": [
        "Area and volume",
        "Lines, angles, and triangles",
        "Right triangles and trigonometry",
        "Circles"
    ]
}


ENG_SUB_TOPICS={
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


SUB_TOPICS=MATH_SUB_TOPICS | ENG_SUB_TOPICS


SUB_TOPIC_TIME={
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
    "One-variable data: Distributions and measures of center and spread": 75,
    "Two-variable data: Models and scatterplots": 90,
    "Probability and conditional probability": 90,
    "Inference from sample statistics and margin of error": 105,
    "Evaluating statistical claims: Observational studies and experiments": 90,

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
    "Easy": "E",
    "Medium": "M",
    "Hard": "H"
}


FULL_TEMPLATE={
    "subjects": ["Math", "English"],

    "questionCount": {
        "Linear equations in one variable": 1,
        "Linear functions": 1,
        "Linear equations in two variables": 1,
        "Systems of two linear equations in two variables": 1,
        "Linear inequalities in one or two variables": 1,

        "Nonlinear functions": 1,
        "Nonlinear equations in one variable and systems of equations in two variables": 1,
        "Equivalent expressions": 1,

        "Ratios, rates, proportional relationships, and units": 1,
        "Percentages": 1,
        "One-variable data: Distributions and measures of center and spread": 1,
        "Two-variable data: Models and scatterplots": 1,
        "Probability and conditional probability": 1,
        "Inference from sample statistics and margin of error": 1,
        "Evaluating statistical claims: Observational studies and experiments": 1,

        "Area and volume": 1,
        "Lines, angles, and triangles": 1,
        "Right triangles and trigonometry": 1,
        "Circles": 1,

        "Rhetorical Synthesis": 1,
        "Transitions": 1,
        "Boundaries": 1,
        "Form, Structure, and Sense": 1,
        "Central Ideas and Details": 1,
        "Inferences": 1,
        "Command of Evidence": 1,
        "Words in Context": 1,
        "Cross-Text Connections": 1,
        "Text Structure and Purpose": 1
    },

    "difficulties": ["E", "M", "H"],
    "timer": 2346
}


FULL_EM1={
    "subjects": ["English"],

    "questionCount": {
        "Central Ideas and Details": 2,
        "Inferences": 2,
        "Command of Evidence": 3,

        "Words in Context": 3,
        "Cross-Text Connections": 2,
        "Text Structure and Purpose": 3,

        "Rhetorical Synthesis": 3,
        "Transitions": 2,

        "Boundaries": 4,
        "Form, Structure, and Sense": 3
    },

    "difficulties": ["E", "M"],
    "timer": 1920
}


FULL_EM2={
    "subjects": ["English"],

    "questionCount": {
        "Central Ideas and Details": 2,
        "Inferences": 2,
        "Command of Evidence": 3,

        "Words in Context": 3,
        "Cross-Text Connections": 2,
        "Text Structure and Purpose": 3,

        "Rhetorical Synthesis": 3,
        "Transitions": 2,

        "Boundaries": 4,
        "Form, Structure, and Sense": 3
    },

    "difficulties": ["M", "H"],
    "timer": 1920
}


FULL_MM1={
    "subjects": ["Math"],

    "questionCount": {
        "Linear equations in one variable": 2,
        "Linear functions": 2,
        "Linear equations in two variables": 1,
        "Systems of two linear equations in two variables": 2,
        "Linear inequalities in one or two variables": 1,

        "Nonlinear functions": 3,
        "Nonlinear equations in one variable and systems of equations in two variables": 3,
        "Equivalent expressions": 2,

        "Ratios, rates, proportional relationships, and units": 1,
        "One-variable data: Distributions and measures of center and spread": 1,
        "Two-variable data: Models and scatterplots": 1,

        "Right triangles and trigonometry": 1,
        "Circles": 1,
        "Lines, angles, and triangles": 1
    },

    "difficulties": ["E", "M"],
    "timer": 2100
}


FULL_MM2={
    "subjects": ["Math"],

    "questionCount": {
        "Linear equations in one variable": 2,
        "Linear functions": 2,
        "Linear equations in two variables": 1,
        "Systems of two linear equations in two variables": 2,
        "Linear inequalities in one or two variables": 1,

        "Nonlinear functions": 3,
        "Nonlinear equations in one variable and systems of equations in two variables": 3,
        "Equivalent expressions": 2,

        "Ratios, rates, proportional relationships, and units": 1,
        "One-variable data: Distributions and measures of center and spread": 1,
        "Two-variable data: Models and scatterplots": 1,

        "Right triangles and trigonometry": 1,
        "Circles": 1,
        "Lines, angles, and triangles": 1
    },

    "difficulties": ["M", "H"],
    "timer": 2100
}


FULL_TEST_MODULES={
    "EM1": FULL_EM1,
    "EM2": FULL_EM2,
    "MM1": FULL_MM1,
    "MM2": FULL_MM2
}