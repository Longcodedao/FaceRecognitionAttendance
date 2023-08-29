import useDB
from datetime import datetime

classroom_DB = useDB.db['class']

class_data = [
    {"class_name": "Design Thinking",
     "class_code": "BEB13116", 
     "start_time": datetime.strptime("11:00:00", "%H:%M:%S"),
     "end_time": datetime.strptime("12:30:00","%H:%M:%S")
    },

    {"class_name": "Artificial Intelligence",
     "class_code": "CSB35037", 
     "start_time": datetime.strptime("11:30:00", "%H:%M:%S"),
     "end_time": datetime.strptime("13:00:00","%H:%M:%S")
    },
]

classroom_DB.insert_many(class_data)
print("Data inserted successfully")