# Initial testing (Fake and pretty) data
_TESTS = {
    'patients' : [
        {
            'fname' : 'John',
            'lname' : 'Doe',
            'nric' : 'G1234567N',
            'gender' : 'Male',
            'dob' : '1998-01-01',
            'phone' : '12345678'
        },
        {
            'fname' : 'Hieu',
            'lname' : 'None',
            'nric' : 'G1778418N',
            'gender' : 'Male',
            'dob' : '2000-04-30',
            'phone' : '88720435'
        },
        {
            'fname' : 'Funk',
            'lname' : 'Uptown',
            'nric' : 'G6969699F',
            'gender' : 'Male',
            'dob' : '1996-06-09',
            'phone' : '69696969'
        },
        {
            'fname' : 'Mai',
            'lname' : 'Dung',
            'nric' : 'C1989365G',
            'gender' : 'Female',
            'dob' : '2000-11-03',
            'phone' : '98877889'
        },
        {
            'fname' : 'Lap',
            'lname' : 'Lacian',
            'nric' : 'G1998201N',
            'gender' : 'Female',
            'dob' : '2000-04-30',
            'phone' : '88720303'
        }
    ],
    'diagnosis' : [
        {
            'nric' : 'G1234567N',
            'xray' : '../../misc/test/positive/MIDRC-RICORD-1C-419639-000002-10161-0.png'
        },
        {
            'nric' : 'G1234567N',
            'xray' : '../../misc/test/positive/MIDRC-RICORD-1C-419639-000025-04760-0.png'
        },
        {
            'nric' : 'G1234567N',
            'xray' : '../../misc/test/negative/02002619-3dea-4038-8d4d-458db30ed8de.png'
        },
        {
            'nric' : 'G1778418N',
            'xray' : '../../misc/test/positive/MIDRC-RICORD-1C-419639-000025-81112-0.png'
        },
        {
            'nric' : 'G1778418N',
            'xray' : '../../misc/test/negative/070c921f-171c-420c-915b-e49e3f600c38.png'
        },
        {
            'nric' : 'G6969699F',
            'xray' : '../../misc/test/negative/02002619-3dea-4038-8d4d-458db30ed8de.png'
        },
        {
            'nric' : 'G6969699F',
            'xray' : '../../misc/test/positive/MIDRC-RICORD-1C-419639-000025-56207-0.png'
        },
        {
            'nric' : 'C1989365G',
            'xray' : '../../misc/test/positive/MIDRC-RICORD-1C-419639-000025-39552-1.png'
        },
        {
            'nric' : 'C1989365G',
            'xray' : '../../misc/test/negative/080f2b35-fcd5-473e-864b-a7dea3054cc7.png'
        },
        {
            'nric' : 'G1998201N',
            'xray' : '../../misc/test/positive/MIDRC-RICORD-1C-419639-000025-39552-1.png'
        },
        {
            'nric' : 'G1998201N',
            'xray' : '../../misc/test/negative/05d3817a-5535-4e77-8dda-d4412e496c81.png'
        }
    ]
}

# Test cases for (Fake and ugly) create-records
_CREATE_RECORDS_CASES = [
    {
        'description' : 'Test case #1',
        'payload' : {
            'fname' : 'John',
            'lname' : 'Doe',
            'nric' : 'G1234567N',
            'gender' : 'Male',
            'dob' : '1998-01-01',
            'phone' : '12345678'
        }
    },
]