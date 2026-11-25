import csv
import json
import random
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent

def generate_customer_reviews():
    """Text classification dataset: Customer feedback with 3 sentiment classes."""
    reviews = [
        # Positive
        ("The quality of this product exceeded all my expectations! Fast delivery and great build.", "Positive", 5, "Electronics"),
        ("Absolutely fantastic customer service. They resolved my return request within two hours.", "Positive", 5, "Support"),
        ("Best purchase I have made this year. Intuitive design, sleek finish, and durable materials.", "Positive", 5, "Electronics"),
        ("Works seamlessly right out of the box. Highly recommended for everyday professional use.", "Positive", 5, "Office"),
        ("Incredible value for money. The battery life lasts twice as long as advertised.", "Positive", 5, "Hardware"),
        ("Super happy with the order! Shipped securely and arrived two days ahead of schedule.", "Positive", 4, "Logistics"),
        ("Very comfortable and ergonomic. My back pain has significantly reduced since using this chair.", "Positive", 5, "Furniture"),
        ("Clear and detailed user manual. Set up took less than ten minutes with zero hassle.", "Positive", 4, "Home"),
        ("Outstanding sound quality and deep bass. Cancels out ambient noise perfectly on flights.", "Positive", 5, "Audio"),
        ("Five stars! Durable zipper, waterproof fabric, and fits my 15-inch laptop securely.", "Positive", 5, "Apparel"),
        # Neutral
        ("The item arrived as described. Standard packaging, average build quality for the price.", "Neutral", 3, "General"),
        ("Decent functionality but the companion mobile application requires frequent reconnecting.", "Neutral", 3, "Software"),
        ("Acceptable performance overall, though the color appears slightly darker than shown online.", "Neutral", 3, "Apparel"),
        ("Fair value. Does what it says, but do not expect luxury materials or premium finishes.", "Neutral", 3, "Home"),
        ("Delivery took five days which is standard. Product works fine without any major issues.", "Neutral", 3, "Logistics"),
        ("Average sound profile. Good for podcasts and meetings, but lacks bass for music.", "Neutral", 3, "Audio"),
        ("Setup was okay. A few confusing diagrams in the instructions, but figured it out eventually.", "Neutral", 3, "Office"),
        ("Product functions as expected. Neither exceptionally great nor particularly bad.", "Neutral", 3, "General"),
        ("The fit is okay, slightly tight around the shoulders but wearable.", "Neutral", 3, "Apparel"),
        ("Adequate battery life. Lasts around six hours before needing a recharge.", "Neutral", 3, "Hardware"),
        # Negative
        ("Extremely disappointed. The device stopped charging completely after only three days of use.", "Negative", 1, "Hardware"),
        ("Terrible customer support. Sent three emails over two weeks without any response whatsoever.", "Negative", 1, "Support"),
        ("Poor build quality. The plastic bracket snapped during initial installation.", "Negative", 1, "Home"),
        ("Does not match the product photos. Cheap fabric, loose stitching, and wrong color delivered.", "Negative", 1, "Apparel"),
        ("Package arrived damaged with the internal seal broken. Item was missing the charging cable.", "Negative", 1, "Logistics"),
        ("Severe latency and frequent Bluetooth disconnections. Virtually unusable for video calls.", "Negative", 1, "Audio"),
        ("Overpriced for the flimsy materials used. Feels like it will break within a month.", "Negative", 2, "Office"),
        ("The software constantly crashes upon launch. Requested an immediate full refund.", "Negative", 1, "Software"),
        ("Battery drains in less than one hour on standby mode. Completely unacceptable performance.", "Negative", 1, "Hardware"),
        ("Misleading specifications. Stated as waterproof but suffered water damage from light rain.", "Negative", 1, "Electronics")
    ]
    # Expand to 90 balanced rows
    records = []
    idx = 1
    for mult in range(3):
        for text, sentiment, rating, cat in reviews:
            records.append({
                "review_id": f"REV-{idx:04d}",
                "review_text": text if mult == 0 else f"Order #{idx}: {text}",
                "sentiment": sentiment,
                "rating": rating,
                "product_category": cat
            })
            idx += 1

    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "customer_reviews.csv", index=False)
    print(f"Generated Customer Reviews dataset: {len(df)} rows.")

def generate_credit_risk():
    """Tabular classification dataset: Credit risk and loan default."""
    rng = random.Random(42)
    records = []
    for i in range(1, 151):
        age = rng.randint(21, 65)
        emp_type = rng.choice(["Salaried", "Self-Employed", "Contractor", "Unemployed"])
        income = round(rng.uniform(25000, 150000), -2)
        credit_score = rng.randint(350, 850)
        loan_amount = round(rng.uniform(5000, 60000), -2)
        debt_to_income = round(loan_amount / max(1, income), 2)
        
        # Determine risk realistically
        if credit_score < 580 or debt_to_income > 0.5 or emp_type == "Unemployed":
            risk = "High" if rng.random() < 0.85 else "Low"
        else:
            risk = "Low" if rng.random() < 0.85 else "High"

        records.append({
            "applicant_id": f"APP-{i:04d}",
            "age": age,
            "employment_type": emp_type,
            "annual_income": income,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "debt_to_income": debt_to_income,
            "default_risk": risk
        })

    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "credit_risk_tabular.csv", index=False)
    print(f"Generated Credit Risk Tabular dataset: {len(df)} rows.")

def generate_house_prices():
    """Tabular regression dataset: Real estate property valuation."""
    rng = random.Random(101)
    records = []
    for i in range(1, 121):
        sqft = rng.randint(800, 4500)
        beds = rng.choice([1, 2, 3, 4, 5])
        baths = rng.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
        zone = rng.choice(["Urban", "Suburban", "Rural"])
        year = rng.randint(1975, 2024)
        
        # Calculate continuous price (in thousands)
        zone_mult = {"Urban": 1.4, "Suburban": 1.1, "Rural": 0.8}[zone]
        price = round(((sqft * 0.12) + (beds * 15) + (baths * 20) + ((year - 1970) * 1.5)) * zone_mult + rng.uniform(-15, 15), 1)

        records.append({
            "property_id": f"PROP-{i:04d}",
            "square_feet": sqft,
            "bedrooms": beds,
            "bathrooms": baths,
            "location_zone": zone,
            "year_built": year,
            "price_thousands": price
        })

    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "house_prices_regression.csv", index=False)
    print(f"Generated House Prices Regression dataset: {len(df)} rows.")

def generate_unlabeled_clinical_notes():
    """Text unlabeled dataset: Medical observation transcripts."""
    notes = [
        "Patient presents with mild respiratory congestion and low-grade pyrexia. Chest auscultation clear bilaterally.",
        "Follow-up visit for post-operative surgical site evaluation. Healing appropriately with no signs of erythema.",
        "Routine cardiovascular checkup. Resting blood pressure recorded at 122/80 mmHg. Electrocardiogram normal.",
        "Neurological examination confirms intact cranial nerves. Patient reports intermittent tension headaches.",
        "Endocrine management consultation. Fasting plasma glucose maintained within normal therapeutic limits.",
        "Dermatological lesion evaluation on left forearm. Consistent with benign seborrheic keratosis.",
        "Orthopedic review of right knee joint following athletic strain. Range of motion within functional baseline.",
        "Gastroenterology outpatient review. Symptomatic improvement noted following dietary modification protocol.",
        "Ophthalmology screening indicates mild ocular dryness. Prescribed preservative-free lubricating drops.",
        "Pediatric developmental milestone review. Growth parameters tracking along the 65th percentile consistently."
    ]
    records = []
    for i in range(1, 51):
        note = notes[(i - 1) % len(notes)]
        dept = ["General Practice", "Cardiology", "Neurology", "Pediatrics", "Dermatology"][(i - 1) % 5]
        records.append({
            "note_id": f"MED-{i:04d}",
            "clinical_notes": note if i <= 10 else f"Encounter #{i}: {note}",
            "department": dept
        })

    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "clinical_notes_unlabeled.csv", index=False)
    print(f"Generated Unlabeled Clinical Notes dataset: {len(df)} rows.")

if __name__ == "__main__":
    generate_customer_reviews()
    generate_credit_risk()
    generate_house_prices()
    generate_unlabeled_clinical_notes()
