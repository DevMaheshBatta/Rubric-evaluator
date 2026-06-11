"""
Rubric definitions for the Mini Answer Evaluator.
Each rubric has keywords for matching, criteria, and max marks.
"""

RUBRICS = [
    {
        "id": "physics_class12",
        "subject": "Physics",
        "level": "Class 12",
        "keywords": [
            "force", "velocity", "acceleration", "momentum", "energy", "power",
            "newton", "gravity", "friction", "electric", "magnetic", "current",
            "voltage", "resistance", "circuit", "wave", "frequency", "amplitude",
            "refraction", "reflection", "lens", "mirror", "photon", "electron",
            "nucleus", "proton", "neutron", "radioactive", "thermodynamics",
            "pressure", "density", "motion", "work", "potential", "kinetic",
            "capacitor", "inductor", "semiconductor", "diode", "transistor",
        ],
        "criteria": [
            {
                "name": "Definition / Concept",
                "description": "Correct definition or conceptual explanation is provided",
                "max_marks": 1,
            },
            {
                "name": "Formula / Mathematical Expression",
                "description": "Relevant formula(s) stated correctly with proper notation",
                "max_marks": 1,
            },
            {
                "name": "Derivation / Steps",
                "description": "Logical derivation or step-by-step working shown",
                "max_marks": 1,
            },
            {
                "name": "Numerical Accuracy",
                "description": "Correct substitution of values and accurate final answer with units",
                "max_marks": 1,
            },
            {
                "name": "Diagram / Graph (if applicable)",
                "description": "Relevant diagram, graph, or illustration described or drawn",
                "max_marks": 1,
            },
        ],
        "max_marks": 5,
    },
    {
        "id": "mathematics_class12",
        "subject": "Mathematics",
        "level": "Class 12",
        "keywords": [
            "integral", "derivative", "differentiate", "integrate", "matrix",
            "determinant", "vector", "probability", "permutation", "combination",
            "function", "limit", "continuity", "differential", "equation",
            "trigonometry", "sine", "cosine", "tangent", "logarithm", "exponential",
            "binomial", "sequence", "series", "arithmetic", "geometric",
            "polynomial", "quadratic", "linear", "coordinate", "geometry",
            "circle", "ellipse", "parabola", "hyperbola", "calculus",
        ],
        "criteria": [
            {
                "name": "Correct Method / Approach",
                "description": "Appropriate mathematical method or theorem selected",
                "max_marks": 1,
            },
            {
                "name": "Step-by-Step Working",
                "description": "Clear, logical, and complete intermediate steps shown",
                "max_marks": 2,
            },
            {
                "name": "Correct Final Answer",
                "description": "Accurate final answer obtained",
                "max_marks": 1,
            },
            {
                "name": "Units / Notation",
                "description": "Correct mathematical notation, units, and sign conventions used",
                "max_marks": 1,
            },
        ],
        "max_marks": 5,
    },
    {
        "id": "english_class10",
        "subject": "English",
        "level": "Class 10",
        "keywords": [
            "poem", "poet", "stanza", "rhyme", "metaphor", "simile", "theme",
            "character", "author", "plot", "story", "novel", "passage", "prose",
            "paragraph", "essay", "language", "grammar", "vocabulary", "meaning",
            "literary", "figure", "speech", "tone", "mood", "symbolism", "imagery",
            "comprehension", "extract", "narrator", "protagonist", "alliteration",
            "personification", "onomatopoeia", "hyperbole", "irony", "satire",
        ],
        "criteria": [
            {
                "name": "Explanation of Key Points",
                "description": "Main ideas or key points from the text are correctly identified and explained",
                "max_marks": 2,
            },
            {
                "name": "Clarity of Expression",
                "description": "Answer is written in clear, coherent sentences",
                "max_marks": 1,
            },
            {
                "name": "Use of Textual Evidence",
                "description": "Relevant quotes, examples, or references from the text are used",
                "max_marks": 1,
            },
            {
                "name": "Language Quality",
                "description": "Correct grammar, spelling, and appropriate vocabulary used",
                "max_marks": 1,
            },
        ],
        "max_marks": 5,
    },
    {
        "id": "chemistry_class12",
        "subject": "Chemistry",
        "level": "Class 12",
        "keywords": [
            "atom", "molecule", "element", "compound", "reaction", "bond",
            "ionic", "covalent", "oxidation", "reduction", "acid", "base",
            "pH", "solution", "concentration", "mole", "molar", "catalyst",
            "equilibrium", "enthalpy", "entropy", "organic", "inorganic",
            "carbon", "hydrogen", "oxygen", "nitrogen", "periodic", "valence",
            "electron", "orbital", "hybridization", "isomer", "polymer",
            "electrolysis", "galvanic", "cell", "electrode",
        ],
        "criteria": [
            {
                "name": "Chemical Concept / Definition",
                "description": "Correct definition or concept accurately stated",
                "max_marks": 1,
            },
            {
                "name": "Chemical Equation / Structure",
                "description": "Balanced chemical equation or structural formula correctly written",
                "max_marks": 1,
            },
            {
                "name": "Mechanism / Steps",
                "description": "Reaction mechanism or logical steps explained correctly",
                "max_marks": 1,
            },
            {
                "name": "Numerical / Calculation",
                "description": "Correct calculation with proper units and significant figures",
                "max_marks": 1,
            },
            {
                "name": "Application / Example",
                "description": "Practical application or real-world example cited",
                "max_marks": 1,
            },
        ],
        "max_marks": 5,
    },
    {
        "id": "biology_class12",
        "subject": "Biology",
        "level": "Class 12",
        "keywords": [
            "cell", "organism", "dna", "rna", "protein", "gene", "chromosome",
            "evolution", "ecology", "photosynthesis", "respiration", "reproduction",
            "nervous", "hormone", "enzyme", "immune", "digestion", "circulation",
            "mitosis", "meiosis", "heredity", "mutation", "species", "ecosystem",
            "food chain", "population", "adaptation", "organ", "tissue",
            "membrane", "nucleus", "mitochondria", "chloroplast", "ribosome",
        ],
        "criteria": [
            {
                "name": "Definition / Scientific Term",
                "description": "Correct biological definition or term explained",
                "max_marks": 1,
            },
            {
                "name": "Process / Mechanism",
                "description": "Biological process described with correct sequence of steps",
                "max_marks": 2,
            },
            {
                "name": "Diagram / Labelling",
                "description": "Relevant diagram described or drawn with correct labels",
                "max_marks": 1,
            },
            {
                "name": "Examples / Applications",
                "description": "Appropriate examples or real-world applications cited",
                "max_marks": 1,
            },
        ],
        "max_marks": 5,
    },
    {
        "id": "history_class10",
        "subject": "History / Social Science",
        "level": "Class 10",
        "keywords": [
            "war", "revolution", "empire", "colonial", "independence", "treaty",
            "civilization", "culture", "economy", "trade", "nationalism", "democracy",
            "government", "political", "social", "movement", "leader", "century",
            "cause", "effect", "impact", "reform", "industrial", "ww1", "ww2",
            "worldwar", "agriculture", "urbanization", "geography", "map", "region",
            "historical", "history", "battles", "invasion", "occupation", "protest",
            "freedom", "slavery", "monarchy", "republic", "parliament", "constitution",
            "imperialism", "colonialism", "partition", "mughal", "british", "french",
        ],
        "criteria": [
            {
                "name": "Factual Accuracy",
                "description": "Key dates, names, and events mentioned correctly",
                "max_marks": 2,
            },
            {
                "name": "Cause and Effect",
                "description": "Cause-and-effect relationships between events explained",
                "max_marks": 1,
            },
            {
                "name": "Logical Structure",
                "description": "Answer is organized logically with clear introduction and conclusion",
                "max_marks": 1,
            },
            {
                "name": "Language Quality",
                "description": "Clear, grammatically correct writing with appropriate terminology",
                "max_marks": 1,
            },
        ],
        "max_marks": 5,
    },
    # ── FALLBACK ──────────────────────────────────────────────────────────────
    {
        "id": "generic_fallback",
        "subject": "General / Fallback",
        "level": "Any",
        "keywords": [],          # matches when nothing else does
        "criteria": [
            {
                "name": "Relevance to the Question",
                "description": "Answer directly addresses what was asked",
                "max_marks": 1,
            },
            {
                "name": "Coverage of Key Points",
                "description": "All important points required by the question are covered",
                "max_marks": 2,
            },
            {
                "name": "Clarity of Explanation",
                "description": "Explanation is clear, easy to follow, and well-structured",
                "max_marks": 1,
            },
            {
                "name": "Language Quality",
                "description": "Correct grammar, appropriate vocabulary, and logical flow",
                "max_marks": 1,
            },
        ],
        "max_marks": 5,
    },
]
