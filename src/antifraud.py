import numpy as np


# Read csv file of History transactions and create history dictionnary    
#lines = np.genfromtxt("/Users/yvesbell/Documents/digital-wallet/paymo_input/batch_payment.txt", delimiter=",", dtype=None)
lines = np.genfromtxt("./paymo_input/batch_payment.txt", delimiter=",", dtype=None)
my_dict_hist = dict()

# Read csv file of future transactions and create dictionnary    
lines2 = np.genfromtxt("./paymo_input/stream_payment.txt", delimiter=",", dtype=None, comments='@@@')
my_dict_trans = dict()

# Load dictionnary of Id's with corresponding transactions friends list
for i in range(len(lines)):
    if i == 0:
        continue
        
    if lines[i][1] in my_dict_hist.keys():
        temp = my_dict_hist[lines[i][1]]
        my_dict_hist[lines[i][1]] = temp + [lines[i][2]]
        continue
        
    my_dict_hist[lines[i][1]] = [lines[i][2]]
    
# Load dictionnary of Id's with corresponding future transactions friends list
for i in range(len(lines2)):
    if i == 0:
        continue 
             
    my_dict_trans[lines2[i][1]] = lines2[i][2]
    
      
 
# Function to return a list of friends based on historical transaction
def returnFriends(id):
    friendslist = []
    for key in my_dict_hist:
        if key == id:
            friendslist = my_dict_hist[key]
            break
    return friendslist
    
# return extended friends list
def returnExtendedFriends(id):
    friendslist = returnFriends(id)
    Extended_friendslist = returnFriends(id)
    
    for key in my_dict_hist:
        if key in friendslist:
            continue
        
        if id in my_dict_hist[key]:
            Extended_friendslist = Extended_friendslist + [key]
        #
    return Extended_friendslist
        
# return extended friends Degree3
def returnExtendedFriends_degree3(id):
    friendslist = returnExtendedFriends(id)
    Extended_friendslist = returnExtendedFriends(id)
    
    for key in my_dict_hist:
        if key in friendslist:
            continue
            
        if id in my_dict_hist[key]:
            Extended_friendslist = Extended_friendslist + [key]
        
    return Extended_friendslist
    

# return extended friends Degree4
def returnExtendedFriends_degree4(id):
    friendslist = returnExtendedFriends_degree3(id)
    Extended_friendslist = returnExtendedFriends_degree3(id)
    
    for key in my_dict_hist:
        if key in friendslist:
            continue
            
        if id in my_dict_hist[key]:
            Extended_friendslist = Extended_friendslist + [key]
        
    return Extended_friendslist
        
    
    
    

# Function for feature 1, if two ids are friends or have had transactions before
def feature1(id1, id2):
    result = ''
    friendlist1 = returnFriends(id1)
    friendlist2 = returnFriends(id2)
    
    if ((id1 in friendlist2) or (id2 in friendlist1)):
        result = 'trusted'
    else:
        result = 'unverified'
    return result
    
# Feature 2
def feature2(id1, id2):
    result = 'unverified'
    Extended_friendslist1 = returnExtendedFriends(id1)
    Extended_friendslist2 = returnExtendedFriends(id2)
    
    
    if (feature1(id1, id2) == 'trusted'):
        result = 'trusted'
    else:
        for i in Extended_friendslist1:
            if i in Extended_friendslist2:
                result = 'trusted'
                break
            else:
                result = 'unverified'
    return result
    
# Feature 3
def feature3(id1, id2):
    result = 'unverified'
    Extended_friendslist1 = returnExtendedFriends_degree3(id1)
    Extended_friendslist2 = returnExtendedFriends_degree3(id2)
    
    
    if (feature2(id1, id2) == 'trusted'):
        result = 'trusted'
    else:
        for i in Extended_friendslist1:
            if i in Extended_friendslist2:
                result = 'trusted'
                break
            else:
                result = 'unverified'
    return result
    
# Feature 4
def feature4(id1, id2):
    result = 'unverified'
    Extended_friendslist1 = returnExtendedFriends_degree4(id1)
    Extended_friendslist2 = returnExtendedFriends_degree4(id2)
    
    
    if (feature3(id1, id2) == 'trusted'):
        result = 'trusted'
    else:
        for i in Extended_friendslist1:
            if i in Extended_friendslist2:
                result = 'trusted'
                break
            else:
                result = 'unverified'
    return result
    
# Loop thru transaction dict and output to file 1 (feature 1)
fw = open('./paymo_output/output1.txt', 'w')
for key in my_dict_trans:
    fw.write(feature1(key, my_dict_trans[key]) + '\n')
fw.close()

# Loop thru transaction dict and output to file 2 (feature 2)
fw2 = open('./paymo_output/output2.txt', 'w')
for key in my_dict_trans:
    fw2.write(feature2(key, my_dict_trans[key]) + '\n')
fw2.close()

# Loop thru transaction dict and output to file 3 (feature 3)
fw3 = open('./paymo_output/output3.txt', 'w')
for key in my_dict_trans:
    fw3.write(feature4(key, my_dict_trans[key]) + '\n')
fw3.close()
    
        
 
    