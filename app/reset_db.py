import db

if __name__ == "__main__":

    import os
    os.system("mysql < ../create_db.sql")

    # User
    ujp = db.insert(table='User', username="ujp", password="tst",
                    fullname="Ujjwal Pandey")
    mkim = db.insert(table='User', username="mkim", password="bap", fullname="Misu Kim")
    yliow = db.insert(table='User', username="yliow", password="knuth",
                      fullname="Dr. Yihsiang Liow")

    # Friend
    um = db.insert(table='Friend', User1_id=ujp['id'], User2_id=mkim['id'])
    mu = db.insert(table='Friend', User1_id=mkim['id'], User2_id=ujp['id'])
    uy = db.insert(table='Friend', User1_id=ujp['id'], User2_id=yliow['id'])

    # TAGS
    landmarks = db.insert(table='Tag', line='Landmarks')
    nature = db.insert(table='Tag', line='Nature')
    food = db.insert(table='Tag', line='Food')
    entertainment = db.insert(table='Tag', line='Entertainment')
    transportation = db.insert(table='Tag', line='Transportation')
    lodging = db.insert(table='Tag', line='Lodging')

    # PERMISSIONS
    public = db.insert(table='Perm', category='Public')
    private = db.insert(table='Perm', category='Private')
    friends = db.insert(table='Perm', category='Friends')
    followers = db.insert(table='Perm', category='Followers')

    # TRAVEL DESTINATIONS
    nepal = db.insert(table='TravelDest', title='Nepal')
    korea = db.insert(table='TravelDest', title='Korea')
    singapore = db.insert(table='TravelDest', title='Singapore')

    # Articles
    visit_nepal = db.insert(table='Article',
                            User_id=ujp['id'],
                            title='Glorious Nepal',
                            body='Visit Nepal when you can!!')
    visit_nepal_nature_tag = db.insert(table='Article_Tag',
                                       Article_id=visit_nepal['id'],
                                       Tag_id=nature['id'])
    # visit_nepal_food_tag = db.insert(table='Article_Tag',
    #                                  Article_id=visit_nepal['id'],
    #                                  Tag_id=food['id'])
    visit_nepal_perm = db.insert(table='Article_Perm',
                                 Article_id=visit_nepal['id'],
                                 Perm_id=public['id'])
    visit_nepal_TravelDest = db.insert(table='Article_TravelDest',
                                       Article_id=visit_nepal['id'],
                                       TravelDest_id=nepal['id'])

    everest = db.insert(table='Article',
                        User_id=ujp['id'],
                        title='Majestic Everest',
                        body='Tallest mountain in the world towers over Nepal and Tibet.')
    everest_nature_tag = db.insert(table='Article_Tag',
                                   Article_id=everest['id'],
                                   Tag_id=nature['id'])
    everest_perm = db.insert(table='Article_Perm',
                             Article_id=everest['id'],
                             Perm_id=followers['id'])
    everest_TravelDest = db.insert(table='Article_TravelDest',
                                   Article_id=everest['id'],
                                   TravelDest_id=nepal['id'])

    octopus = db.insert(table='Article',
                        User_id=mkim['id'],
                        title='Tasty Octopus',
                        body='Live octopus is yummy!')
    octopus_food_tag = db.insert(table='Article_Tag',
                                   Article_id=octopus['id'],
                                   Tag_id=food['id'])
    octopus_perm = db.insert(table='Article_Perm',
                             Article_id=octopus['id'],
                             Perm_id=friends['id'])
    octopus_TravelDest = db.insert(table='Article_TravelDest',
                                   Article_id=octopus['id'],
                                   TravelDest_id=korea['id'])


    singapore_tt = db.insert(table='Article',
                             User_id=yliow['id'],
                             title='Table Tennis in Singapore',
                             body='Come play ping pong next time you are in Singapore.')
    singapore_tt_entertainment_tag = db.insert(table='Article_Tag',
                                               Article_id=singapore_tt['id'],
                                               Tag_id=entertainment['id'])
    singapore_tt_perm = db.insert(table='Article_Perm',
                                  Article_id=singapore_tt['id'],
                                  Perm_id=followers['id'])
    singapore_tt_TravelDest = db.insert(table='Article_TravelDest',
                                        Article_id=singapore_tt['id'],
                                        TravelDest_id=singapore['id'])


