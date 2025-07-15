# this is the processing file 
# establishes connection with database and provides methods to get data from different tables
# database: 
import sqlite3, os, json
#get the path to the present working dir
loc =os.getcwd()
path =loc+'/fantasy_cricket.db'
# print(path)

try: 
    con = sqlite3.connect(path)
    mycursor = con.cursor()

except Exception as e:
    print(e)
# get match details
def getmatches(m_name=None):
    try:
        if m_name:
            sql = "select m_id from matches where m_name='"+m_name+"';"
            mycursor.execute(sql)
            record = mycursor.fetchone()
            return(record)
            
        else:
            sql = "select * from matches;"
            mycursor.execute(sql)
            records = mycursor.fetchall()
            return(records)
            
    except Exception as e:
        print(e)
        
# get all teams
def getteams():
    try:
        sql = "select * from teams;"
        mycursor.execute(sql)
        records = mycursor.fetchall()
        return(records)
    
    except Exception as e:
        print(e)
        
# get specific team details
def getteamdetails(team, m_id=None):
    try:
        if m_id and team:
            sql = "select t_players from teams where t_name ='"+team+"'and match_id="+str(m_id)+" ;"
            # print(sql)
        elif team:
            sql = "select * from teams where t_name ='"+team+"';"
        mycursor.execute(sql)
        record = mycursor.fetchone()
        return(record)
    except Exception as e:
        print(e)

# get players of a team for available player list
def get_players(team_id, ctg):
    try:
        # get the team with this t_id
        sql = "select t_players from teams where t_id ="+str(team_id)+";"
        mycursor.execute(sql)
        record = mycursor.fetchone()
        if record:
            t_players = json.loads(record[0])
            if t_players:
                #list not empty
                if len(t_players) == 1:
                    sql = 'select p_id, p_name, p_ctg, p_value from player_stats where p_ctg="'+ str(ctg)+'" and p_id not in ('+str(t_players[0]) +');'
                else:
                    sql = 'select p_id, p_name, p_ctg, p_value from player_stats where p_ctg="'+ str(ctg)+'" and p_id not in '+str(tuple(t_players)) +';'
                # print(sql)
                 
            else:
                sql = 'select p_id, p_name, p_ctg, p_value from player_stats where p_ctg ="'+ str(ctg)+'";'
            mycursor.execute(sql)
            records = mycursor.fetchall()
            return(records)            

    except Exception as e:
        print(e)
    
# insert team into teams table
def set_team(name,m_id):
    try:
    
        sql = "insert into teams(t_name, match_id) values('"+name+"', "+m_id+")"
        # print(sql)
        mycursor.execute(sql)
        con.commit()
        return 1
    except Exception as  e:
        print(e)
        con.rollback()
# get player details by id 
def get_players_by_id(p_id_list):
    try:
        if p_id_list:
            if len(p_id_list)== 1:
               sql = 'select p_id, p_name, p_ctg, p_value from player_stats where p_id in ('+str(p_id_list[0]) +');' 
            else:
                sql = 'select p_id, p_name, p_ctg, p_value from player_stats where p_id in '+str(tuple(p_id_list)) +';'
            # print(sql)
            mycursor.execute(sql)
            records = mycursor.fetchall()
            return(records)
        
    except Exception as e:
        print(e)

# update playerlist in team
def update_player_list(t_id,p_id, t_value, flag = 1):
    try:
        
        sql = 'select t_players from teams where t_id= '+str(t_id)+';'
        mycursor.execute(sql)
        t_players = mycursor.fetchone()
        player_list = eval(t_players[0])
        # print(player_list)
        if flag == 1:
            player_list.append(int(p_id))
        if flag == 2:
            # when player is removed from team players
            player_list.remove(int(p_id))

        list(set(player_list))
        # # print(player_list)
        
        # # # update the new player list
        sql = "update teams set t_players ='"+str(player_list)+"' , t_value ="+str(t_value)+" where t_id="+str(t_id)+";"
        # print(sql)
        mycursor.execute(sql)
        con.commit()
        
    
    except Exception as e:
        print(e)
        con.rollback()

def get_player_stats(id, m_id):
    try: 
        sql= "select p_id, scored, fours, sixes, wkts,catches, runouts, faced from p_match_performance where p_id = "+str(id)+" and match_id = "+str(m_id)+";"
        # print(sql)
        mycursor.execute(sql)
        record = mycursor.fetchone()
        players = {
            "p_id": record[0],
            "scored": record[1],
            "fours": record[2],
            "sixes":record[3],
            "wkts": record[4],
            "catches": record[5],
            "stumping": record[6],
            "faced":record[7]
        }
    
        return(players)
    except Exception as e:
        print(e)
