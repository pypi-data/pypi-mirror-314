=====
Usage
=====

To use Python client for dataquality.pl in a project::

    from dq import DQClient, JobConfig


    dq = DQClient('https://app.dataquality.pl', user='<USER_EMAIL>', token='<API_TOKEN>')


API token can be obtain on the page "Moje konto".


Account
=======

Check account status::

    account = dq.account_status()

    print(account.email)          # user email
    print(account.balance)        # account balance
    print(account.total_records)  # processed records


Jobs
====

List jobs
---------
::

    jobs = dq.list_jobs()

    for job in jobs:
        print(job.id)                # job id
        print(job.name)              # human readable job name
        print(job.status)            # job status
        print(job.start_date)        # job start date
        print(job.end_date)          # job end date
        print(job.source_records)    # how many records were applied
        print(job.processed_records) # how many records were processed
        print(job.price)             # price for processed records


Create new job
--------------
::

    input_data = '''"ID","ADRES"
    6876,"34-404, PYZÓWKA, PODHALAŃSKA 100"
    '''

    job_config = JobConfig('my job')
    job_config.input_format(field_separator=',', text_delimiter='"')
    job_config.input_column(0, name='ID', function='PRZEPISZ')
    job_config.input_column(1, name='ADRES', function='DANE_OGOLNE')
    job_config.module_std(address=1)
    job_config.extend(gus=True, geocode=True)

    job = dq.submit_job(job_config, input_data=input_data)                                         # with data in a variable

    job = dq.submit_job(job_config, input_file='my_file.csv')                                      # with data inside file

    print(job.id)
    print(job.name)
    print(job.status)
    ...

Create new deduplication job
--------------
::

	input_data = '''unikalne_id;imie_i_nazwisko;kod_pocztowy;miejscowosc;adres;email;tel;CrmContactNumber;data
	1;Jan Kowalski;37-611;Cieszanów ;Dachnów 189;abc@wp.pl;605936000;abc123;2017-11-08 12:00:00.000
	2;Adam Mickiewicz Longchamps de Berier;66-400;Gorzów Wlkp.;Widok 24;qqq@ft.com;48602567000;a2b2c2;2017-11-08 12:00:00.000
	3;Barbara Łęcka;76-200;Słupsk;Banacha 7;bb@gazeta.pl;79174000;emc2;2017-11-08 12:00:00.000
	4;KAROL NOWAK;22-122;LEŚNIOWICE;RAKOLUPY DU—E 55;kn@ll.pp;0;f112358;2017-11-08 12:00:00.000
	5;Anna Maria Jopek;34-722;Podwilk;Podwilk 464;amj@gmail.com;606394000;eipi10;2017-11-08 12:00:00.000
	6;Mariusz Robert;37-611;Cieszanów ;Dachnów 189;abc@wp.pl;605936000;abc123;2017-11-08 12:00:00.000
	'''

	job_config = JobConfig('pr2')
	job_config.input_format(field_separator=';', text_delimiter='"')
	job_config.input_column(0, name='unikalne_id', function='ID_REKORDU')
	job_config.input_column(1, name='imie_i_nazwisko', function='IMIE_I_NAZWISKO')
	job_config.input_column(2, name='kod_pocztowy', function='KOD_POCZTOWY')
	job_config.input_column(3, name='miejscowosc', function='MIEJSCOWOSC')
	job_config.input_column(4, name='adres', function='ULICA_NUMER_DOMU_I_MIESZKANIA')
	job_config.input_column(5, name='email', function='EMAIL1')
	job_config.input_column(6, name='tel', function='TELEFON1')
	job_config.input_column(7, name='CrmContactNumber', function='PRZEPISZ')
	job_config.input_column(8, name='data', function='CZAS_AKTUALIZACJI')
	job_config.deduplication(on=True)
	job_config.module_std(address=True, names=True, contact=True)
	job_config.extend(gus=True, geocode=True, diagnostic=True)

	job = dq.submit_job(job_config, input_data=input_data)

	print(job)
	...

Available column functions:

* addresses
    * KOD_POCZTOWY
    * MIEJSCOWOSC
    * ULICA_NUMER_DOMU_I_MIESZKANIA
    * ULICA
    * NUMER_DOMU
    * NUMER_MIESZKANIA
    * NUMER_DOMU_I_MIESZKANIA
    * WOJEWODZTWO
    * POWIAT
    * GMINA
* names
    * IMIE
    * NAZWISKO
    * NAZWA_PODMIOTU
    * IMIE_I_NAZWISKO
* people/companies
    * PESEL
    * NIP
    * REGON
* contact
    * EMAIL1
    * EMAIL2
    * TELEFON1
    * TELEFON2
* dates
    * DATA_URODZENIA
    * CZAS_AKTUALIZACJI
* mixed
    * DANE_OGOLNE
* id
    * ID_REKORDU
* others
    * PRZEPISZ
    * POMIN


To process input columns, you must enable the corresponding module. Method module_std is used to set active modules:

* address
* names
* contact
* id_numbers

For address module to be started it is necessary to ensure at least one column with the role listed below:

* DANE_OGOLNE
* KOD_POCZTOWY
* MIEJSCOWOSC

Analogously for other modules:

* names require one of
    * DANE_OGOLNE
    * IMIE
    * NAZWISKO
    * IMIE_I_NAZWISKO
    * NAZWA_PODMIOTU

* contact
    * DANE_OGOLNE
    * EMAIL1
    * EMAIL2
    * TELEFON1
    * TELEFON2

* id
    * DANE_OGOLNE
    * PESEL
    * NIP
    * REGON


Check job state
---------------
::

    state = dq.job_state('3f14e25e-9f6d-41ff-a4cb-942743a37b73')  # input parameter: job id

    print(state)                                                  # 'WAITING' or 'FINISHED'


Cancel job
----------
::

    dq.cancel_job('3f14e25e-9f6d-41ff-a4cb-942743a37b73')  # input parameter: job id


Retrieve job report
-------------------
::

    report = dq.job_report('3f14e25e-9f6d-41ff-a4cb-942743a37b73')  # input parameter: job id

    print(report.quality_issues)
    print(report.quality_names)
    print(report.results)


Save job results
----------------
::

    dq.job_results('3f14e25e-9f6d-41ff-a4cb-942743a37b73', 'output.csv')


Delete job and its results
--------------------------
::

    dq.delete_job('3f14e25e-9f6d-41ff-a4cb-942743a37b73')  # input parameter: job id
