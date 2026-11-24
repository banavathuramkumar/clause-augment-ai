"""
Script to generate standard contract clauses dataset for ClauseAugment AI.
Includes 10 standard legal categories with 20 realistic, varied clauses per category (total 200 clauses).
"""
import csv
import json
import os

CLAUSE_DATA = {
    "Confidentiality": [
        "The Receiving Party shall maintain in strict confidence and shall not disclose to any third party any Confidential Information of the Disclosing Party without prior written consent.",
        "Confidential Information shall include all technical, financial, commercial, or other proprietary data disclosed either orally or in writing.",
        "The obligations of confidentiality shall survive the termination or expiration of this Agreement for a period of five (5) years.",
        "The Receiving Party agrees to restrict access to Confidential Information solely to its employees, advisors, and contractors who have a need to know.",
        "Confidential Information does not include information that is or becomes publicly known through no breach of this Agreement by the Receiving Party.",
        "Upon written request of the Disclosing Party, the Receiving Party shall promptly return or certify destruction of all copies of Confidential Information.",
        "Neither party shall disclose the existence or terms of this Agreement without the prior written approval of the other party.",
        "Each party agrees to use the same degree of care to protect the other party's Confidential Information as it uses to protect its own confidential materials of like nature.",
        "If the Receiving Party is legally compelled by court order to disclose any Confidential Information, it shall provide prompt written notice to the Disclosing Party.",
        "Proprietary materials exchanged under this Agreement shall remain the exclusive property of the disclosing entity.",
        "The recipient shall not reverse engineer, decompile, or disassemble any trade secret or software provided hereunder.",
        "All notes, analyses, and summaries prepared by the recipient incorporating Confidential Information shall remain subject to the terms of this Agreement.",
        "Nothing herein shall obligate either party to disclose any particular item of confidential or proprietary information.",
        "The confidentiality restrictions herein shall not apply to information independently developed by the Receiving Party without reference to Confidential Information.",
        "Both parties acknowledge that unauthorized disclosure of trade secrets may cause irreparable harm for which monetary damages alone would be inadequate.",
        "The Receiving Party shall immediately notify the Disclosing Party upon discovery of any loss or unauthorized disclosure of Confidential Information.",
        "The recipient shall mark all physical and digital copies of confidential files with appropriate protective legends.",
        "No license under any patent, copyright, or trademark is granted or implied by the disclosure of Confidential Information.",
        "Trade secrets shall remain subject to confidentiality obligations indefinitely or for as long as they qualify as trade secrets under applicable law.",
        "Any disclosure of Confidential Information to an permitted contractor shall require a written non-disclosure agreement with terms at least as restrictive as this Section."
    ],
    "Indemnification": [
        "The Vendor agrees to indemnify, defend, and hold harmless the Customer and its officers, directors, and employees from and against any third-party claims arising out of negligence.",
        "Each party shall defend and indemnify the other party against all losses, damages, liabilities, and expenses arising from any material breach of this Agreement.",
        "The Contractor shall indemnify the Client against any claims alleging that the Deliverables infringe or misappropriate any patent, copyright, or trade secret of a third party.",
        "Indemnification obligations under this Section are conditioned upon the indemnified party giving prompt written notice of any covered claim.",
        "The indemnifying party shall have sole control over the defense and settlement of any indemnifiable claim, provided that settlement does not admit liability.",
        "The Service Provider will indemnify the Customer against all fines, penalties, and direct losses resulting from the Service Provider's violation of applicable privacy laws.",
        "The indemnified party shall have the right to participate in the defense of any claim at its own expense with counsel of its choosing.",
        "Customer shall indemnify and hold harmless Licensor from any third-party claims arising from Customer's unauthorized modification of the Licensed Software.",
        "The obligations under this Article shall apply regardless of whether the claim or liability is caused in part by an indemnified party.",
        "In no event shall the indemnifying party settle any claim requiring an admission of guilt or financial contribution without the indemnified party's consent.",
        "The Supplier shall indemnify the Buyer against all product liability claims arising from design defects or manufacturing deficiencies in the supplied goods.",
        "The Tenant shall indemnify and hold harmless the Landlord against all claims for personal injury or property damage occurring on the leased premises.",
        "Each party's indemnification liabilities shall be reduced proportionately to the extent that the other party contributed to the loss.",
        "The Consultant shall indemnify and hold the Company harmless against any tax assessment or withholding liability arising from contractor classification.",
        "The indemnifying party shall promptly reimburse the indemnified party for all reasonable legal fees and costs incurred in enforcing this indemnification right.",
        "Licensor agrees to defend Licensee against any allegation that the Cloud Service infringes an existing United States patent.",
        "If an infringement claim occurs, the indemnifying party may procure for the indemnified party the right to continue using the affected service.",
        "This indemnification provision shall survive any expiration, cancellation, or termination of this Agreement.",
        "The obligations of defense and indemnification set forth herein are subject to the indemnified party providing reasonable cooperation and documentation.",
        "The Distributor shall defend and indemnify Manufacturer against all claims resulting from false advertising or misrepresentations made by Distributor."
    ],
    "Termination": [
        "Either party may terminate this Agreement without cause upon giving sixty (60) days prior written notice to the other party.",
        "Either party may terminate this Agreement immediately upon written notice if the other party commits a material breach that remains uncured for thirty (30) days.",
        "This Agreement shall automatically terminate upon the bankruptcy, insolvency, or appointment of a receiver for either party.",
        "Upon termination of this Agreement, all licenses granted hereunder shall immediately cease and determine.",
        "Termination of this Agreement shall not relieve either party from liability for obligations or payments accrued prior to the effective date of termination.",
        "The Company may terminate this Agreement immediately if the Contractor engages in gross negligence, fraud, or willful misconduct.",
        "Customer may terminate any Statement of Work for convenience upon thirty (30) days advance written notice to Service Provider.",
        "Upon expiration or termination, each party shall promptly return or destroy all property and Confidential Information belonging to the other party.",
        "Sections concerning Confidentiality, Indemnification, Limitation of Liability, and Governing Law shall survive any termination of this Agreement.",
        "In the event of termination by Customer for cause, Service Provider shall refund any prepaid and unused fees on a pro-rata basis.",
        "Failure by either party to enforce any right upon breach shall not waive the right to terminate for subsequent breaches.",
        "If a Force Majeure event continues for more than ninety (90) consecutive days, either party may terminate this Agreement upon written notice.",
        "The Licensor may suspend or terminate access to the Platform immediately upon notice if Licensee fails to pay past-due invoices within ten (10) days.",
        "Upon termination, Customer shall pay Service Provider for all authorized services performed and reimbursable expenses incurred up to the termination date.",
        "This Agreement will expire at the end of the Initial Term unless renewed in writing by mutual consent of both parties.",
        "Either party may terminate this Agreement if the other party undergoes a change of control involving a direct competitor.",
        "Termination notices must be sent via certified mail or tracked courier to the designated representatives listed in Section 14.",
        "The expiration or termination of this Agreement shall be without prejudice to any other remedies available at law or in equity.",
        "Service Provider may terminate services if continuing performance would violate applicable statutory regulations or export control rules.",
        "Upon notice of termination, Contractor shall immediately stop work unless directed otherwise in writing by the Client."
    ],
    "Liability": [
        "In no event shall either party be liable to the other for any indirect, incidental, consequential, special, or punitive damages.",
        "Except for gross negligence or willful misconduct, each party's total aggregate liability under this Agreement shall not exceed the fees paid in the preceding twelve (12) months.",
        "The limitations of liability set forth in this Section shall apply regardless of whether an action is brought in contract, tort, or warranty.",
        "Neither party shall be liable for lost profits, loss of data, loss of business reputation, or cost of substitute procurement.",
        "The maximum cumulative liability of Licensor for all claims arising out of this Agreement shall be strictly capped at the amount paid by Licensee.",
        "The exclusions of liability in this Section shall not apply to breaches of confidentiality obligations or indemnification duties.",
        "Customer agrees that Service Provider shall have no liability for outages or service degradations caused by third-party telecommunication carriers.",
        "To the maximum extent permitted by applicable law, all warranties not expressly set forth herein are disclaimed.",
        "No action or claim arising out of this Agreement may be brought by either party more than one (1) year after the cause of action accrued.",
        "Each party acknowledges that the fees charged reflect the allocation of risk and agreed liability caps between the parties.",
        "Neither party's liability for death or personal injury resulting from its own negligence shall be limited or excluded.",
        "In no event shall the Company be liable for any punitive or exemplary damages arising out of performance or non-performance.",
        "The liability caps herein shall apply in the aggregate to all claims and shall not be cumulative across multiple incidents.",
        "Licensor shall not be responsible for any damages resulting from unauthorized access or modification to Customer data by third parties.",
        "Under no circumstances shall the Consultant's aggregate liability exceed the total compensation actually received under the relevant Statement of Work.",
        "The parties agree that the economic terms of this contract depend upon the enforceability of these risk limitation provisions.",
        "Neither party excludes liability for fraud, fraudulent misrepresentation, or any liability that cannot be excluded under applicable law.",
        "Any statutory rights that cannot be waived by private contract shall remain unaffected by the limitations set forth in this Article.",
        "The aggregate liability cap shall increase to two times the annual contract value solely in the event of an adjudicated data breach.",
        "Service Provider disclaims any express or implied guarantee that the system will be entirely error-free or uninterrupted."
    ],
    "Governing Law": [
        "This Agreement shall be governed by, and construed in accordance with, the laws of the State of Delaware, without giving effect to conflicts of law principles.",
        "The parties hereby submit to the exclusive jurisdiction and venue of the federal and state courts located in New York County, New York.",
        "This contract and all claims arising out of or related to it shall be governed by the laws of England and Wales.",
        "Any dispute arising from this contract shall be adjudicated exclusively in the competent courts of San Francisco, California.",
        "The United Nations Convention on Contracts for the International Sale of Goods shall not apply to this Agreement.",
        "This Agreement shall be interpreted and enforced under the laws of the Commonwealth of Massachusetts.",
        "The parties irrevocably waive any objection to the venue of any action brought in the specified forum based on inconvenient forum.",
        "Each party hereby irrevocably waives any right to a trial by jury in any litigation arising out of this Agreement.",
        "This contract shall be construed under the laws of the State of Texas, without regard to its choice of law provisions.",
        "All legal proceedings arising out of this Agreement shall be instituted in the District Court for the Northern District of Illinois.",
        "The validity, construction, and performance of this Agreement shall be governed by the laws of the State of Washington.",
        "The parties agree that service of process in any legal action may be delivered by registered mail to their principal office address.",
        "This Agreement is made under and shall be governed in all respects by the laws of the Federal Republic of Germany.",
        "The governing law of this Agreement shall be the laws of the State of New York, excluding its conflict of laws rules.",
        "Both parties consent to personal jurisdiction in the state courts situated in Travis County, Texas.",
        "Nothing in this Agreement shall prevent either party from seeking preliminary injunctive relief in any court of competent jurisdiction.",
        "This Agreement shall be governed by the substantive laws of the Province of Ontario and the federal laws of Canada applicable therein.",
        "The choice of governing law shall remain effective regardless of the location where services are rendered or received.",
        "The parties agree that this contract shall be deemed executed and performable in the State of Georgia.",
        "Any legal action brought by Customer against Service Provider must be commenced in the courts of Wilmington, Delaware."
    ],
    "Payment": [
        "Customer shall pay all undisputed invoices within thirty (30) days from the date of invoice receipt.",
        "Late payments shall accrue interest at the rate of one and a half percent (1.5%) per month or the maximum rate permitted by law.",
        "All fees specified in this Agreement are exclusive of applicable federal, state, local, or value-added taxes.",
        "In the event of a disputed charge, Customer shall notify Service Provider in writing within fifteen (15) days of the invoice date.",
        "Customer shall be responsible for all sales, use, excise, and withholding taxes associated with purchases under this Agreement.",
        "Payment shall be made by electronic funds transfer or Automated Clearing House (ACH) to the bank account specified by Vendor.",
        "If any undisputed invoice remains unpaid for more than forty-five (45) days, Vendor reserves the right to suspend performance.",
        "All payments under this Agreement shall be made in United States Dollars ($ USD) unless agreed otherwise in writing.",
        "Service Provider may increase recurring subscription fees upon renewal by providing at least sixty (60) days advance notice.",
        "Customer shall reimburse Service Provider for all pre-approved out-of-pocket travel and lodging expenses incurred in performing services.",
        "Failure to dispute an invoice within thirty (30) days of issuance shall constitute acceptance of the invoiced amount.",
        "All fees paid under this Agreement are non-refundable except as expressly provided in the Termination for Cause section.",
        "The Client shall pay a non-refundable deposit of twenty-five percent (25%) upon execution of this contract.",
        "Invoices shall be generated on a monthly billing cycle and transmitted electronically to the designated billing contact.",
        "Customer agrees to pay all reasonable collection agency fees and attorney fees incurred in collecting delinquent accounts.",
        "No deduction, setoff, or withholding of payments shall be made by Customer on account of any alleged counterclaim.",
        "Contractor shall submit detailed timesheets and expense receipts supporting all time-and-materials payment requests.",
        "Any credit balance granted to Customer must be utilized within twelve (12) months or it shall expire without cash value.",
        "Milestone payments shall be disbursed within fourteen (14) days following written acceptance of each agreed milestone deliverable.",
        "Taxes withheld by Customer pursuant to foreign statutory mandates shall be accompanied by official tax receipts."
    ],
    "Force Majeure": [
        "Neither party shall be liable for failure or delay in performance caused by circumstances beyond its reasonable control, including acts of God, war, and epidemics.",
        "If a Force Majeure event prevents performance for more than thirty (30) days, the non-affected party may terminate this Agreement.",
        "Events of Force Majeure include strikes, lockouts, supply shortages, civil unrest, natural disasters, power failures, and government directives.",
        "The party experiencing a Force Majeure event shall promptly notify the other party in writing stating the nature and expected duration.",
        "The affected party shall use all reasonable efforts to mitigate the effects of the Force Majeure event and resume performance quickly.",
        "Payment obligations for services rendered prior to the Force Majeure event shall not be excused or delayed by this provision.",
        "A Force Majeure event shall automatically extend the performance deadline for a period equal to the duration of the disruption.",
        "Neither party shall be in default if non-performance is caused by severe acts of nature such as floods, earthquakes, or hurricanes.",
        "Failure of subcontractors or software providers shall not constitute Force Majeure unless caused by an independent event beyond their control.",
        "If governmental sanctions or trade embargoes prevent product delivery, the affected party's obligations shall be temporarily suspended.",
        "War, hostilities, invasion, terrorist acts, or widespread cyberattacks against national infrastructure shall constitute Force Majeure events.",
        "Upon cessation of the Force Majeure condition, the affected party shall give immediate notice and resume full contractual performance.",
        "The doctrine of impossibility or frustration of purpose shall be interpreted consistent with the express allocations of this Article.",
        "Both parties agree to establish disaster recovery protocols to minimize potential disruptions caused by Force Majeure incidents.",
        "The right to invoke Force Majeure shall not apply to conditions resulting from a party's financial insolvency or inability to pay.",
        "In the event of an epidemic or public health lockdown, both parties shall negotiate in good faith to adapt delivery schedules.",
        "Strikes or industrial disputes restricted solely to the workforce of the affected party shall not be considered Force Majeure.",
        "Notice of Force Majeure must be delivered within five (5) business days of the occurrence of the disruptive event.",
        "Either party may procure temporary substitute services from third parties during an ongoing Force Majeure suspension.",
        "The obligations of confidentiality shall remain in full force and effect during any period of Force Majeure."
    ],
    "Dispute Resolution": [
        "Any dispute, controversy, or claim arising out of this Agreement shall be settled by binding arbitration in accordance with AAA rules.",
        "Prior to initiating litigation or arbitration, senior executives of both parties shall meet in good faith to resolve the dispute amicably.",
        "Arbitration proceedings shall be conducted by a single neutral arbitrator in New York City, and the proceedings shall be held in English.",
        "The decision and award of the arbitrator shall be final, non-appealable, and enforceable in any court of competent jurisdiction.",
        "The prevailing party in any dispute resolution proceeding shall be entitled to recover reasonable attorney fees and associated legal costs.",
        "All claims must be brought in the parties' individual capacity, and neither party may act as a plaintiff or class member in any class proceeding.",
        "The parties agree that informal mediation administered by JAMS shall be a mandatory prerequisite to filing any formal legal claim.",
        "Each party consents that arbitration discoveries shall be strictly limited to essential document exchanges to reduce litigation expenses.",
        "Nothing herein shall prevent either party from seeking emergency injunctive relief from a court of equity to prevent irreparable harm.",
        "The arbitrator shall have no authority to award punitive damages or damages in excess of the contractual limitations of liability.",
        "Any mediation or arbitration proceedings shall remain strictly confidential between the parties and their legal representatives.",
        "If the parties cannot agree upon a single arbitrator within thirty (30) days, each party shall appoint one arbitrator and the two shall select a third.",
        "The statutes of limitations applicable to any claim shall be tolled during the pendency of formal mediation proceedings.",
        "The costs and administrative fees of the arbitration tribunal shall initially be shared equally by both parties pending the final award.",
        "Disputes regarding intellectual property infringement or breach of non-disclosure terms are exempt from mandatory arbitration.",
        "The arbitration hearing shall conclude within sixty (60) days of arbitrator appointment unless extended for good cause shown.",
        "Each party agrees that any award rendered by the arbitral panel may be entered for judgment in any court having subject jurisdiction.",
        "The governing law specified in Section 12 shall govern the interpretation and validity of this arbitration agreement.",
        "Notice of dispute must set forth the factual basis of the claim and the specific contractual remedies demanded.",
        "Informal executive negotiations must continue for at least twenty (20) business days before either party may commence mediation."
    ],
    "Intellectual Property": [
        "All intellectual property rights in the software, documentation, and underlying technology remain the exclusive property of Licensor.",
        "Customer is granted a non-exclusive, non-transferable, revocable license to access and use the Platform during the Subscription Term.",
        "All inventions, work product, and deliverables created by Contractor under this Agreement shall constitute 'works made for hire'.",
        "Client retains all right, title, and interest in and to Customer Data and Customer's pre-existing intellectual property.",
        "Licensee shall not modify, copy, distribute, sublicense, or create derivative works based upon the proprietary software.",
        "Any feedback, suggestions, or enhancements submitted by Customer may be used by Service Provider without restriction or royalty obligations.",
        "Contractor hereby assigns to Company all right, title, and ownership in all patents, copyrights, and trade secrets developed hereunder.",
        "Service Provider retains all rights in general knowledge, skills, ideas, concepts, and reusable code developed during the engagement.",
        "No title or ownership of any proprietary software or patent is transferred to Customer under this Agreement.",
        "Licensee shall not remove, alter, or obscure any copyright notices, trademark notices, or proprietary legends affixed to the materials.",
        "Customer grants Vendor a limited license to host, process, and transmit Customer Data solely to perform the services.",
        "The documentation, user manuals, and training assets supplied by Licensor are protected by international copyright conventions.",
        "If work product does not legally qualify as a work made for hire, Contractor irrevocably assigns all rights therein to Client.",
        "Each party shall retain sole ownership of all pre-existing intellectual property developed prior to the effective date of this Agreement.",
        "Vendor warrants that it possesses all necessary intellectual property licenses and permissions required to perform the services.",
        "Customer shall not facilitate any third party to scrape, harvest, or extract algorithmic models or databases from the Service.",
        "All registered trademarks, service marks, and logos remain the exclusive property of their respective trademark registrants.",
        "Contractor agrees to execute all assignment documentation and patent declarations necessary to perfect Company's intellectual property rights.",
        "Any open-source software embedded in the solution is licensed strictly pursuant to its governing open-source license agreement.",
        "Unauthorized reproduction or decompilation of Licensor's proprietary software shall constitute copyright infringement and breach of contract."
    ],
    "Data Protection": [
        "Each party shall comply with all applicable data privacy laws, including the General Data Protection Regulation (GDPR) and CCPA.",
        "Service Provider shall implement appropriate technical and organizational measures to safeguard personal data against unauthorized access.",
        "Service Provider shall notify Customer in writing within forty-eight (48) hours of becoming aware of any confirmed personal data breach.",
        "Customer represents that it has obtained all necessary consents and authorizations required to transfer personal data to Service Provider.",
        "Service Provider shall process personal data solely on documented instructions from Customer and for the purposes specified herein.",
        "Upon termination of the services, Service Provider shall delete or return all personal data in its custody unless retention is required by law.",
        "Service Provider shall not transfer personal data across international borders without implementing approved standard contractual clauses.",
        "Customer retains the right to conduct annual security audits of Service Provider's data handling practices upon reasonable notice.",
        "Service Provider shall ensure that personnel authorized to process personal data have committed themselves to confidentiality.",
        "Service Provider shall assist Customer in responding to data subject requests to exercise rights of access, rectification, or erasure.",
        "Sub-processors may only be engaged with prior written authorization of Customer and under equivalent data protection terms.",
        "Personal data shall be encrypted both in transit using TLS 1.3 and at rest using industry-standard AES-256 encryption.",
        "Each party shall maintain comprehensive records of data processing activities as mandated by statutory compliance guidelines.",
        "Service Provider shall cooperate with supervisory authorities and provide access to its data security documentation upon request.",
        "Customer shall not transmit special category sensitive data unless explicitly agreed in a separate Data Processing Addendum.",
        "Service Provider shall carry out periodic vulnerability scans and independent penetration testing on all data processing infrastructure.",
        "In the event of a security incident, Service Provider shall take immediate remediation steps to contain and mitigate the vulnerability.",
        "The parties agree that the Data Processing Addendum (DPA) attached hereto as Exhibit B is hereby incorporated into this Agreement.",
        "Service Provider shall maintain documented incident response plans and test them at least once every twelve (12) months.",
        "Personal data shall be retained only for as long as necessary to fulfill the operational purposes set forth in this contract."
    ]
}

def generate_datasets():
    csv_rows = []
    json_records = []
    
    clause_counter = 1
    for category, clauses in CLAUSE_DATA.items():
        for clause in clauses:
            clause_id = f"CLS-{clause_counter:04d}"
            record = {
                "clause_id": clause_id,
                "clause_text": clause.strip(),
                "clause_type": category
            }
            csv_rows.append(record)
            json_records.append(record)
            clause_counter += 1
            
    # Save CSV
    csv_path = os.path.join("backend", "datasets", "sample_contract_clauses.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["clause_id", "clause_text", "clause_type"])
        writer.writeheader()
        writer.writerows(csv_rows)
        
    # Save JSON
    json_path = os.path.join("backend", "datasets", "sample_contract_clauses.json")
    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(json_records, f, indent=2)
        
    print(f"Generated {len(csv_rows)} clauses across {len(CLAUSE_DATA)} categories.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved JSON: {json_path}")

if __name__ == "__main__":
    generate_datasets()
