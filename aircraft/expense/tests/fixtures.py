from expense.models import Person, Flight

def fixtures_3_return_flights_in_3_months():
    owner1 = Person.objects.create(name=u'Owner 1', owner=True)
    owner2 = Person.objects.create(name=u'Owner 2', owner=True)

    flight1 = Flight.objects.create(
            origin = "SBJD", 
            destiny = "ABCD", 
            start_hobbs = 100.0, 
            mantainance = False, 
            date = "2011-10-12", 
            cycles = 3, 
            end_hobbs = 110.0
        )
    flight1.pax_set.create(owner=owner1, ammount=4)
    
    flight2 = Flight.objects.create(
            origin = "ABCD", 
            destiny = "SBJD", 
            start_hobbs = 110.0, 
            mantainance = False, 
            date = "2011-10-13", 
            cycles = 3, 
            end_hobbs = 120.0
        )
    
    flight3 = Flight.objects.create(
            origin = "SBJD", 
            destiny = "BCDE", 
            start_hobbs = 120.0, 
            mantainance = False, 
            date = "2011-11-12", 
            cycles = 3, 
            end_hobbs = 130.0
        )
    flight3.pax_set.create(owner=owner2, ammount=3)
    
    flight4 = Flight.objects.create(
            origin = "BCDE", 
            destiny = "SBJD", 
            start_hobbs = 130.0, 
            mantainance = False, 
            date = "2011-11-13", 
            cycles = 3, 
            end_hobbs = 140.0
        )
    
    flight5 = Flight.objects.create(
            origin = "SBJD", 
            destiny = "CDEF", 
            start_hobbs = 140.0, 
            mantainance = False, 
            date = "2011-12-12", 
            cycles = 3, 
            end_hobbs = 170.0
        )
    flight5.pax_set.create(owner=owner1, ammount=3)
    flight5.pax_set.create(owner=owner2, ammount=6)
    
    flight6 = Flight.objects.create(
            origin = "CDEF", 
            destiny = "SBJD", 
            start_hobbs = 170.0, 
            mantainance = False, 
            date = "2011-12-13", 
            cycles = 3, 
            end_hobbs = 200.0
        )
    
    flight7 = Flight.objects.create(
            origin = "SBJD", 
            destiny = "MANT", 
            start_hobbs = 200.0, 
            date = "2011-12-20", 
            cycles = 3, 
            end_hobbs = 202.0,
	    mantainance = True
        )

    flight8 = Flight.objects.create(
            origin = "MANT", 
            destiny = "SBJD", 
            start_hobbs = 202.0, 
            date = "2011-12-20", 
            cycles = 3, 
            end_hobbs = 204.0,
	    mantainance = True
        )    
