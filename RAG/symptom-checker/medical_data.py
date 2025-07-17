docs = [
    # Chest Pain
    "Chest pain can indicate heart problems such as angina or heart attack. Angina typically presents as pressure or squeezing sensation, while heart attack pain is often severe and may radiate to the arm, jaw, or back.",
    "Acute chest pain accompanied by shortness of breath, sweating, or nausea requires immediate medical attention as these are warning signs of a possible heart attack.",
    "Chest pain that worsens when breathing or coughing may indicate pleurisy, an inflammation of the tissues that line the lungs and chest cavity.",
    "Reflux or GERD can cause burning chest pain (heartburn) that typically worsens after eating, when lying down, or bending over.",
    "Muscle strain in the chest wall often results from overexertion and may be reproduced by pressing on the affected area or certain movements.",
    "Panic attacks can cause acute chest pain accompanied by rapid heartbeat, shortness of breath, and feelings of impending doom.",
    "Costochondritis, an inflammation of the cartilage connecting ribs to the breastbone, causes localized chest pain that worsens with movement or pressure.",
    
    # Breathing Difficulties
    "Difficulty in breathing can be caused by asthma, pneumonia, or anxiety. Asthma typically presents with wheezing and chest tightness.",
    "Chronic obstructive pulmonary disease (COPD) causes persistent breathing difficulty, especially during physical activity, and often includes chronic cough with mucus.",
    "Pneumonia typically causes difficulty breathing along with fever, chest pain, and productive cough with yellow or green phlegm.",
    "Pulmonary embolism, a blood clot in the lungs, can cause sudden shortness of breath, chest pain, and rapid heartbeat and requires emergency treatment.",
    "Heart failure may cause shortness of breath, especially when lying down (orthopnea) or during physical activity, often accompanied by swelling in the legs.",
    "Anxiety-induced hyperventilation causes rapid, shallow breathing and can lead to tingling in the extremities, lightheadedness, and chest tightness.",
    
    # Abdominal Symptoms
    "Upper abdominal pain that radiates to the back may indicate pancreatitis, especially if accompanied by nausea and worsens after eating.",
    "Right upper quadrant abdominal pain, particularly after fatty meals, could suggest gallbladder issues such as gallstones or cholecystitis.",
    "Lower right abdominal pain with tenderness, fever, and nausea may indicate appendicitis, which requires prompt medical evaluation.",
    "Inflammatory bowel diseases like Crohn's disease or ulcerative colitis can cause chronic abdominal pain, diarrhea, and weight loss.",
    "Irritable bowel syndrome (IBS) typically causes abdominal pain relieved by bowel movements, changes in bowel habits, and bloating.",
    
    # Headaches
    "Tension headaches typically cause mild to moderate pain described as a tight band around the head, often related to stress or muscle tension.",
    "Migraine headaches often present with moderate to severe throbbing pain, typically on one side, and may be accompanied by nausea, vomiting, and sensitivity to light and sound.",
    "Cluster headaches cause excruciating pain around one eye or temple, occur in cycles or clusters, and may be accompanied by eye redness, tearing, and nasal congestion.",
    "Headaches accompanied by fever, stiff neck, confusion, or severe pain that comes on suddenly (thunderclap headache) require immediate medical attention as they may indicate serious conditions.",
    
    # Joint and Muscle Pain
    "Osteoarthritis typically causes joint pain that worsens with activity and improves with rest, often affecting weight-bearing joints like knees and hips.",
    "Rheumatoid arthritis causes joint pain with swelling, stiffness (especially in the morning), and may affect multiple joints symmetrically.",
    "Gout typically presents as sudden, severe joint pain, often in the big toe, accompanied by redness, swelling, and tenderness.",
    "Fibromyalgia causes widespread musculoskeletal pain accompanied by fatigue, sleep, memory, and mood issues.",
    
    # Skin Conditions
    "Eczema causes dry, itchy, red patches of skin that may become scaly, crusty, or weepy, often appearing in the creases of elbows and knees.",
    "Psoriasis typically presents as red, scaly patches with well-defined borders, often on elbows, knees, scalp, and lower back.",
    "Hives appear as raised, itchy welts that can appear and disappear rapidly, often in response to an allergen.",
    "Skin rashes accompanied by fever, spreading rapidly, or appearing after starting a new medication require prompt medical attention.",
]

doc_titles = [
    # Chest Pain
    "Heart-Related Chest Pain",
    "Warning Signs of Heart Attack",
    "Pleurisy and Chest Pain",
    "Chest Pain from Reflux",
    "Chest Muscle Strain",
    "Panic Attack Symptoms",
    "Costochondritis",
    
    # Breathing Difficulties
    "Common Causes of Breathing Difficulty",
    "COPD Symptoms",
    "Pneumonia Symptoms",
    "Pulmonary Embolism",
    "Heart Failure and Breathing",
    "Anxiety-Related Breathing Issues",
    
    # Abdominal Symptoms
    "Pancreatic Pain Patterns",
    "Gallbladder Issues",
    "Appendicitis Warning Signs",
    "Inflammatory Bowel Disease",
    "Irritable Bowel Syndrome",
    
    # Headaches
    "Tension Headache Characteristics",
    "Migraine Headache Patterns",
    "Cluster Headache Features",
    "Headache Warning Signs",
    
    # Joint and Muscle Pain
    "Osteoarthritis Symptoms",
    "Rheumatoid Arthritis Signs",
    "Gout Symptoms",
    "Fibromyalgia Characteristics",
    
    # Skin Conditions
    "Eczema Features",
    "Psoriasis Presentation",
    "Hives Description",
    "Concerning Skin Rashes",
]

symptom_categories = {
    "Chest Pain": range(0, 7),
    "Breathing Difficulties": range(7, 13),
    "Abdominal Symptoms": range(13, 18),
    "Headaches": range(18, 22),
    "Joint and Muscle Pain": range(22, 26),
    "Skin Conditions": range(26, 30)
}