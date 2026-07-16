# utils/college_data.py

EXTENDED_CS_COLLEGES = [
    # Maharashtra
    ("IIT Bombay", "Mumbai", "Premier institute for CS.", "https://www.iitb.ac.in", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 1}),
    ("VJTI Mumbai", "Mumbai", "Top state government college.", "https://vjti.ac.in", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 15}),
    ("SPIT Mumbai", "Mumbai", "Excellent private CS college.", "https://www.spit.ac.in", {"state": "Maharashtra", "region": "West", "type": "Private", "rank": 20}),
    ("COEP Pune", "Pune", "Historic govt engineering college.", "https://www.coep.org.in", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 12}),
    ("PICT Pune", "Pune", "Renowned for CS placements.", "https://pict.edu", {"state": "Maharashtra", "region": "West", "type": "Private", "rank": 25}),
    ("VIT Pune", "Pune", "Top autonomous engineering college.", "https://www.vit.edu", {"state": "Maharashtra", "region": "West", "type": "Private", "rank": 30}),
    ("VNIT Nagpur", "Nagpur", "Top NIT in Maharashtra.", "https://vnit.ac.in", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 10}),
    
    # Karnataka
    ("IISc Bangalore", "Bengaluru", "World-class research in CS/AI.", "https://www.iisc.ac.in", {"state": "Karnataka", "region": "South", "type": "Govt", "rank": 1}),
    ("NITK Surathkal", "Mangaluru", "Premier NIT for CS.", "https://www.nitk.ac.in", {"state": "Karnataka", "region": "South", "type": "Govt", "rank": 5}),
    ("RVCE Bangalore", "Bengaluru", "Top private college in Karnataka.", "https://www.rvce.edu.in", {"state": "Karnataka", "region": "South", "type": "Private", "rank": 15}),
    ("BMSCE Bangalore", "Bengaluru", "Excellent CS programs.", "https://bmsce.ac.in", {"state": "Karnataka", "region": "South", "type": "Private", "rank": 20}),
    ("PES University", "Bengaluru", "Strong focus on modern tech.", "https://pes.edu", {"state": "Karnataka", "region": "South", "type": "Private", "rank": 25}),
    ("MSRIT Bangalore", "Bengaluru", "Renowned engineering institute.", "https://www.msrit.edu", {"state": "Karnataka", "region": "South", "type": "Private", "rank": 30}),
    ("IIIT Bangalore", "Bengaluru", "Specialized in IT and CS.", "https://www.iiitb.ac.in", {"state": "Karnataka", "region": "South", "type": "Govt", "rank": 8}),

    # Delhi
    ("IIT Delhi", "Delhi", "Top-tier IIT.", "https://home.iitd.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 2}),
    ("DTU", "Delhi", "Top state university for engineering.", "https://dtu.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 10}),
    ("NSUT", "Delhi", "Premier CS and IT institute.", "https://www.nsut.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 12}),
    ("IIIT Delhi", "Delhi", "World-class CS research.", "https://www.iiitd.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 8}),
    ("NIT Delhi", "Delhi", "Growing NIT with strong CS.", "https://nitdelhi.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 20}),

    # Tamil Nadu
    ("IIT Madras", "Chennai", "Ranked #1 engineering institute.", "https://www.iitm.ac.in", {"state": "Tamil Nadu", "region": "South", "type": "Govt", "rank": 1}),
    ("NIT Trichy", "Tiruchirappalli", "Best NIT in India.", "https://www.nitt.edu", {"state": "Tamil Nadu", "region": "South", "type": "Govt", "rank": 3}),
    ("Anna University", "Chennai", "Top state university.", "https://www.annauniv.edu", {"state": "Tamil Nadu", "region": "South", "type": "Govt", "rank": 10}),
    ("VIT Vellore", "Vellore", "Premier private engineering university.", "https://vit.ac.in", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 12}),
    ("SRM Institute", "Chennai", "Massive private university.", "https://www.srmist.edu.in", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 18}),
    ("PSG College", "Coimbatore", "Excellent industry placements.", "https://www.psgtech.edu", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 20}),
    ("SSN College", "Chennai", "Top private college in Chennai.", "https://www.ssn.edu.in", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 25}),

    # Telangana
    ("IIT Hyderabad", "Hyderabad", "Modern IIT with great AI department.", "https://www.iith.ac.in", {"state": "Telangana", "region": "South", "type": "Govt", "rank": 5}),
    ("IIIT Hyderabad", "Hyderabad", "Best coding culture in India.", "https://www.iiit.ac.in", {"state": "Telangana", "region": "South", "type": "Govt", "rank": 4}),
    ("NIT Warangal", "Warangal", "Top-tier NIT.", "https://www.nitw.ac.in", {"state": "Telangana", "region": "South", "type": "Govt", "rank": 6}),
    ("CBIT", "Hyderabad", "Premier private institute.", "https://cbit.ac.in", {"state": "Telangana", "region": "South", "type": "Private", "rank": 20}),
    ("VNR VJIET", "Hyderabad", "Excellent CS placements.", "http://www.vnrvjiet.ac.in", {"state": "Telangana", "region": "South", "type": "Private", "rank": 25}),

    # Uttar Pradesh
    ("IIT Kanpur", "Kanpur", "Historic IIT with top CS.", "https://www.iitk.ac.in", {"state": "Uttar Pradesh", "region": "North", "type": "Govt", "rank": 3}),
    ("IIT BHU", "Varanasi", "Prestigious IIT.", "https://www.iitbhu.ac.in", {"state": "Uttar Pradesh", "region": "North", "type": "Govt", "rank": 8}),
    ("MNNIT Allahabad", "Prayagraj", "Top NIT for coding.", "http://www.mnnit.ac.in", {"state": "Uttar Pradesh", "region": "North", "type": "Govt", "rank": 10}),
    ("IIIT Allahabad", "Prayagraj", "Premier IT institute.", "https://www.iiita.ac.in", {"state": "Uttar Pradesh", "region": "North", "type": "Govt", "rank": 12}),
    ("HBTU", "Kanpur", "Top state university.", "https://hbtu.ac.in", {"state": "Uttar Pradesh", "region": "North", "type": "Govt", "rank": 25}),
    ("Amity University", "Noida", "Large private university.", "https://www.amity.edu", {"state": "Uttar Pradesh", "region": "North", "type": "Private", "rank": 40}),

    # West Bengal
    ("IIT Kharagpur", "Kharagpur", "Oldest and largest IIT.", "https://www.iitkgp.ac.in", {"state": "West Bengal", "region": "East", "type": "Govt", "rank": 4}),
    ("Jadavpur University", "Kolkata", "Exceptional ROI and CS dept.", "http://www.jaduniv.edu.in", {"state": "West Bengal", "region": "East", "type": "Govt", "rank": 8}),
    ("NIT Durgapur", "Durgapur", "Premier NIT.", "https://nitdgp.ac.in", {"state": "West Bengal", "region": "East", "type": "Govt", "rank": 15}),
    ("IEM Kolkata", "Kolkata", "Top private college in WB.", "https://iem.edu", {"state": "West Bengal", "region": "East", "type": "Private", "rank": 30}),
    ("Heritage Institute", "Kolkata", "Renowned private institute.", "https://www.heritageit.edu", {"state": "West Bengal", "region": "East", "type": "Private", "rank": 35}),

    # Rajasthan
    ("BITS Pilani", "Pilani", "India's best private engineering university.", "https://www.bits-pilani.ac.in", {"state": "Rajasthan", "region": "North", "type": "Private", "rank": 1}),
    ("IIT Jodhpur", "Jodhpur", "Rising IIT with strong AI focus.", "https://iitj.ac.in", {"state": "Rajasthan", "region": "North", "type": "Govt", "rank": 12}),
    ("MNIT Jaipur", "Jaipur", "Top NIT in Rajasthan.", "http://www.mnit.ac.in", {"state": "Rajasthan", "region": "North", "type": "Govt", "rank": 10}),
    ("LNMIIT", "Jaipur", "Excellent coding culture.", "https://www.lnmiit.ac.in", {"state": "Rajasthan", "region": "North", "type": "Private", "rank": 20}),
    
    # Gujarat
    ("IIT Gandhinagar", "Gandhinagar", "Modern IIT campus.", "https://www.iitgn.ac.in", {"state": "Gujarat", "region": "West", "type": "Govt", "rank": 10}),
    ("NIT Surat", "Surat", "Top NIT in Gujarat.", "https://www.svnit.ac.in", {"state": "Gujarat", "region": "West", "type": "Govt", "rank": 15}),
    ("DA-IICT", "Gandhinagar", "Premier institute for IT.", "https://www.daiict.ac.in", {"state": "Gujarat", "region": "West", "type": "Private", "rank": 12}),
    ("Nirma University", "Ahmedabad", "Top private university.", "https://nirmauni.ac.in", {"state": "Gujarat", "region": "West", "type": "Private", "rank": 25}),

    # Madhya Pradesh
    ("IIT Indore", "Indore", "Top-tier IIT.", "https://www.iiti.ac.in", {"state": "Madhya Pradesh", "region": "Central", "type": "Govt", "rank": 8}),
    ("MANIT Bhopal", "Bhopal", "Premier NIT.", "https://www.manit.ac.in", {"state": "Madhya Pradesh", "region": "Central", "type": "Govt", "rank": 15}),
    ("IIITDM Jabalpur", "Jabalpur", "Design and manufacturing focus.", "https://www.iiitdmj.ac.in", {"state": "Madhya Pradesh", "region": "Central", "type": "Govt", "rank": 20}),
    ("SGSITS Indore", "Indore", "Top state college.", "https://www.sgsits.ac.in", {"state": "Madhya Pradesh", "region": "Central", "type": "Govt", "rank": 30}),

    # Punjab & Haryana
    ("IIT Ropar", "Ropar", "Leading new IIT.", "https://www.iitrpr.ac.in", {"state": "Punjab", "region": "North", "type": "Govt", "rank": 10}),
    ("NIT Jalandhar", "Jalandhar", "Premier NIT.", "https://www.nitj.ac.in", {"state": "Punjab", "region": "North", "type": "Govt", "rank": 20}),
    ("Thapar Institute", "Patiala", "Top private engineering college.", "https://www.thapar.edu", {"state": "Punjab", "region": "North", "type": "Private", "rank": 15}),
    ("NIT Kurukshetra", "Kurukshetra", "Historic NIT.", "https://nitkkr.ac.in", {"state": "Haryana", "region": "North", "type": "Govt", "rank": 12}),
    
    # Rest of India (Assam, Bihar, Odisha, etc.)
    ("IIT Guwahati", "Guwahati", "Top IIT in North East.", "https://www.iitg.ac.in", {"state": "Assam", "region": "North East", "type": "Govt", "rank": 6}),
    ("NIT Silchar", "Silchar", "Top NIT in Assam.", "http://www.nits.ac.in", {"state": "Assam", "region": "North East", "type": "Govt", "rank": 20}),
    ("IIT Patna", "Patna", "Rising IIT.", "https://www.iitp.ac.in", {"state": "Bihar", "region": "East", "type": "Govt", "rank": 15}),
    ("NIT Patna", "Patna", "Premier NIT.", "https://www.nitp.ac.in", {"state": "Bihar", "region": "East", "type": "Govt", "rank": 25}),
    ("IIT Bhubaneswar", "Bhubaneswar", "Modern IIT.", "https://www.iitbbs.ac.in", {"state": "Odisha", "region": "East", "type": "Govt", "rank": 12}),
    ("NIT Rourkela", "Rourkela", "Top NIT in India.", "https://www.nitrkl.ac.in", {"state": "Odisha", "region": "East", "type": "Govt", "rank": 8}),
    ("KIIT", "Bhubaneswar", "Massive private university.", "https://kiit.ac.in", {"state": "Odisha", "region": "East", "type": "Private", "rank": 20}),
]

EXTENDED_CORE_COLLEGES = [
    # Mechanical, Civil, Electrical
    ("IIT Bombay", "Mumbai", "World-class core engineering.", "https://www.iitb.ac.in", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 1}),
    ("COEP Pune", "Pune", "Gold-standard for mechanical and civil.", "https://www.coep.org.in", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 10}),
    ("VJTI Mumbai", "Mumbai", "Historic state college.", "https://vjti.ac.in", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 15}),
    ("IIT Delhi", "Delhi", "Top-tier core programs.", "https://home.iitd.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 2}),
    ("DTU", "Delhi", "Excellent mechanical engineering.", "https://dtu.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 8}),
    ("IIT Madras", "Chennai", "Outstanding core research.", "https://www.iitm.ac.in", {"state": "Tamil Nadu", "region": "South", "type": "Govt", "rank": 1}),
    ("Anna University", "Chennai", "Top state university.", "https://www.annauniv.edu", {"state": "Tamil Nadu", "region": "South", "type": "Govt", "rank": 10}),
    ("NIT Trichy", "Tiruchirappalli", "Premier core placements.", "https://www.nitt.edu", {"state": "Tamil Nadu", "region": "South", "type": "Govt", "rank": 3}),
    ("IIT Kanpur", "Kanpur", "Renowned aerospace and mechanical.", "https://www.iitk.ac.in", {"state": "Uttar Pradesh", "region": "North", "type": "Govt", "rank": 4}),
    ("IIT Kharagpur", "Kharagpur", "Largest core engineering campus.", "https://www.iitkgp.ac.in", {"state": "West Bengal", "region": "East", "type": "Govt", "rank": 5}),
    ("Jadavpur University", "Kolkata", "Exceptional core placements.", "http://www.jaduniv.edu.in", {"state": "West Bengal", "region": "East", "type": "Govt", "rank": 10}),
    ("BITS Pilani", "Pilani", "Excellent private core engineering.", "https://www.bits-pilani.ac.in", {"state": "Rajasthan", "region": "North", "type": "Private", "rank": 6}),
    ("NIT Surathkal", "Mangaluru", "Top core NIT.", "https://www.nitk.ac.in", {"state": "Karnataka", "region": "South", "type": "Govt", "rank": 8}),
    ("NIT Warangal", "Warangal", "Renowned for civil engineering.", "https://www.nitw.ac.in", {"state": "Telangana", "region": "South", "type": "Govt", "rank": 9}),
]

EXTENDED_BBA_COLLEGES = [
    ("IIM Indore", "Indore", "Top IPM program in India.", "https://www.iimidr.ac.in", {"state": "Madhya Pradesh", "region": "Central", "type": "Govt", "rank": 1}),
    ("IIM Rohtak", "Rohtak", "Premier IPM program.", "https://www.iimrohtak.ac.in", {"state": "Haryana", "region": "North", "type": "Govt", "rank": 2}),
    ("Shaheed Sukhdev College of Business Studies", "Delhi", "Best BBA college under DU.", "https://sscbs.du.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 1}),
    ("NMIMS Mumbai", "Mumbai", "Top private BBA.", "https://nmims.edu", {"state": "Maharashtra", "region": "West", "type": "Private", "rank": 3}),
    ("Symbiosis Centre for Management Studies", "Pune", "Tier-1 BBA institute.", "https://www.scmspune.ac.in", {"state": "Maharashtra", "region": "West", "type": "Private", "rank": 4}),
    ("Christ University", "Bengaluru", "Highly reputed management programs.", "https://christuniversity.in", {"state": "Karnataka", "region": "South", "type": "Private", "rank": 5}),
    ("St. Xavier's College", "Mumbai", "Historic college for BMS.", "https://xaviers.edu", {"state": "Maharashtra", "region": "West", "type": "Private", "rank": 6}),
    ("Loyola College", "Chennai", "Top commerce and BBA.", "https://www.loyolacollege.edu", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 8}),
    ("Madras Christian College", "Chennai", "Excellent management degree.", "https://mcc.edu.in", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 10}),
    ("Mount Carmel College", "Bengaluru", "Premier women's college.", "https://mccblr.edu.in", {"state": "Karnataka", "region": "South", "type": "Private", "rank": 12}),
]

EXTENDED_MED_COLLEGES = [
    ("AIIMS New Delhi", "Delhi", "India's #1 medical institute.", "https://www.aiims.edu", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 1}),
    ("PGIMER", "Chandigarh", "Premier medical research.", "http://pgimer.edu.in", {"state": "Chandigarh", "region": "North", "type": "Govt", "rank": 2}),
    ("CMC Vellore", "Vellore", "World-class private medical college.", "https://www.cmch-vellore.edu", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 3}),
    ("NIMHANS", "Bengaluru", "Top neuro science institute.", "https://nimhans.ac.in", {"state": "Karnataka", "region": "South", "type": "Govt", "rank": 4}),
    ("JIPMER", "Puducherry", "Premier medical institute.", "https://jipmer.edu.in", {"state": "Puducherry", "region": "South", "type": "Govt", "rank": 5}),
    ("AFMC Pune", "Pune", "Armed forces medical college.", "https://afmc.nic.in", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 6}),
    ("KMC Manipal", "Manipal", "Top private medical college.", "https://manipal.edu/kmc-manipal.html", {"state": "Karnataka", "region": "South", "type": "Private", "rank": 8}),
    ("Grant Medical College", "Mumbai", "Historic medical college.", "https://www.gmcmumbai.org", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 10}),
    ("Madras Medical College", "Chennai", "Oldest medical college.", "http://www.mmc.ac.in", {"state": "Tamil Nadu", "region": "South", "type": "Govt", "rank": 12}),
    ("King George's Medical University", "Lucknow", "Top medical university in UP.", "https://www.kgmu.org", {"state": "Uttar Pradesh", "region": "North", "type": "Govt", "rank": 15}),
    ("AIIMS Jodhpur", "Jodhpur", "Leading new AIIMS.", "https://www.aiimsjodhpur.edu.in", {"state": "Rajasthan", "region": "North", "type": "Govt", "rank": 18}),
    ("AIIMS Bhubaneswar", "Bhubaneswar", "Leading new AIIMS.", "https://aiimsbhubaneswar.nic.in", {"state": "Odisha", "region": "East", "type": "Govt", "rank": 20}),
]

EXTENDED_ARTS_COLLEGES = [
    ("Hindu College", "Delhi", "Top arts and science college.", "https://hinducollege.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 1}),
    ("Miranda House", "Delhi", "India's top women's college.", "https://mirandahouse.ac.in", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 2}),
    ("St. Stephen's College", "Delhi", "Prestigious arts college.", "https://www.ststephens.edu", {"state": "Delhi", "region": "North", "type": "Govt", "rank": 3}),
    ("Presidency College", "Chennai", "Historic arts college.", "http://www.presidencycollegechennai.ac.in", {"state": "Tamil Nadu", "region": "South", "type": "Govt", "rank": 5}),
    ("Loyola College", "Chennai", "Top private arts college.", "https://www.loyolacollege.edu", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 6}),
    ("St. Xavier's College", "Mumbai", "Iconic arts and humanities.", "https://xaviers.edu", {"state": "Maharashtra", "region": "West", "type": "Private", "rank": 8}),
    ("Fergusson College", "Pune", "Historic arts and science.", "https://www.fergusson.edu", {"state": "Maharashtra", "region": "West", "type": "Govt", "rank": 10}),
    ("Madras Christian College", "Chennai", "Renowned liberal arts.", "https://mcc.edu.in", {"state": "Tamil Nadu", "region": "South", "type": "Private", "rank": 12}),
    ("Christ University", "Bengaluru", "Top psychology and arts.", "https://christuniversity.in", {"state": "Karnataka", "region": "South", "type": "Private", "rank": 15}),
    ("Symbiosis College of Arts and Commerce", "Pune", "Premium arts college.", "https://symbiosiscollege.edu.in", {"state": "Maharashtra", "region": "West", "type": "Private", "rank": 18}),
]
