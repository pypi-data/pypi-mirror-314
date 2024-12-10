Unreleased changes
------------------

Version 0
---------
0.4.18 / 2024-12-10
~~~~~~~~~~~~~~~~~~~
* added oscillations open data

0.4.17 / 2024-11-07
~~~~~~~~~~~~~~~~~~~
* added PMT sample

0.4.16 / 2024-09-30
~~~~~~~~~~~~~~~~~~~
* added summaryslices sample

0.4.15 / 2024-07-03
~~~~~~~~~~~~~~~~~~~
* another orientations.root sample

0.4.14 / 2024-07-03
~~~~~~~~~~~~~~~~~~~
* orientations.root sample

0.4.13 / 2024-05-24
~~~~~~~~~~~~~~~~~~~
* HDF5 sample of a km3astro output file

0.4.12 / 2024-03-26
~~~~~~~~~~~~~~~~~~~
* added a DETX which contains invalid multiline comments

0.4.11 / 2024-02-26
~~~~~~~~~~~~~~~~~~~
* added CLB Swissknife acoustic sample

0.4.10 / 2024-01-26
~~~~~~~~~~~~~~~~~~~
* RBR (mupage) sample added

* DATX sample added
0.4.9 / 2024-01-25
~~~~~~~~~~~~~~~~~~
* DATX sample added

0.4.8 / 2024-01-22
~~~~~~~~~~~~~~~~~~
* another DETX sample file containing the floor == -1 bug

0.4.7 / 2023-10-04
~~~~~~~~~~~~~~~~~~
* yet another online sample file for reco benchmarks and tests

0.4.6 / 2023-10-04
~~~~~~~~~~~~~~~~~~
* added another sample file with 1000 muon cc events for reco benchmarks and tests

0.4.5 / 2023-07-19
~~~~~~~~~~~~~~~~~~
* added an online file with 10 JDAQEvents and a matching DETX

0.4.4 / 2023-05-23
~~~~~~~~~~~~~~~~~~
* PMT efficiency sample added

0.4.4 / 2023-04-24
~~~~~~~~~~~~~~~~~~
* Update GIBUU files

0.4.3 / 2023-01-24
~~~~~~~~~~~~~~~~~~
* DST sample (mainly for ``km3irf``) has been added
* Python 3.9 and 3.10 added to the CI test stage

0.4.0 / 2022-11-07
~~~~~~~~~~~~~~~~~~
* Ditch yapf in favour of black for code style
* Added empty offline ROOT file: ``offline/empty_events.root``
* Removed Python 2.7 support

0.3.7 / 2022-09-20
~~~~~~~~~~~~~~~~~~
* Added multiHead.root to offline example files.

0.3.6 / 2022-07-14
~~~~~~~~~~~~~~~~~~
* Fixes (replaces) the v5.0 ORCA 115-string offline file from 0.3.5

0.3.5 / 2022-07-12
~~~~~~~~~~~~~~~~~~
* v5.0 ORCA 115-string offline file added, triggered and reconstructed with Jpp v16, containing a sub-selection of 10 reconstructed events.

0.3.4 / 2022-06-07
~~~~~~~~~~~~~~~~~~
* Corsika test files added

0.3.3 / 2022-03-24
~~~~~~~~~~~~~~~~~~
* Replaces the gSeaGen file from 0.3.2 which did not
  contain the counter values

0.3.2 / 2022-03-24
~~~~~~~~~~~~~~~~~~
* Added a gSeaGen file with counter values on MC tracks

0.3.1 / 2022-03-23
~~~~~~~~~~~~~~~~~~
* Added DETX v5

0.3.0 / 2022-03-11
~~~~~~~~~~~~~~~~~~
* Added a bunch of astro benchmark files for ORCA and ARCA
* Reordered the columns of the ANTARES astro benchmark files

0.2.30 / 2022-01-14
~~~~~~~~~~~~~~~~~~~
* Fix Error.Arguments field in HV-tuning JSON file for DB API v2

0.2.29 / 2021-10-07
~~~~~~~~~~~~~~~~~~~
* Fix a typo in ANTARES astro coordinate benchmark (moon and sun file)

0.2.28 / 2021-09-15
~~~~~~~~~~~~~~~~~~~
* added nueCC file for tests of Aashowerfit shower reconstruction

0.2.27 / 2021-07-17
~~~~~~~~~~~~~~~~~~~
* Newer version of DST sample added (`orca6...`)

0.2.26 / 2021-06-30
~~~~~~~~~~~~~~~~~~~
* HV-tuning JSON-files added to `db/`
* raw acoustics sample added to `acoustics/`

0.2.25 / 2021-05-15
~~~~~~~~~~~~~~~~~~~
* gseagen v6.0 offline file added

0.2.24 / 2021-04-18
~~~~~~~~~~~~~~~~~~~
* DST sample added

0.2.23 / 2021-02-02
~~~~~~~~~~~~~~~~~~~
* Added a new mupage ARCA sample to hdf5/

0.2.22 / 2021-02-02
~~~~~~~~~~~~~~~~~~~
* geamon samples added

0.2.21 / 2021-02-01
~~~~~~~~~~~~~~~~~~~
* New MUPAGE samples added
* gSeaGen v7 samples added

0.2.20 / 2020-12-03
~~~~~~~~~~~~~~~~~~~
* DETX v4 added

0.2.19 / 2020-11-10
~~~~~~~~~~~~~~~~~~~
* Added L1 timeslice dump of data type 1003 to DAQ

0.2.18 / 2020-11-06
~~~~~~~~~~~~~~~~~~~
* Cleaned up DAQ sample files: old files have been suffixed with _legacy

0.2.17 / 2020-11-06
~~~~~~~~~~~~~~~~~~~
* Removed wrong DAQ samples

0.2.16 / 2020-11-06
~~~~~~~~~~~~~~~~~~~
* Update samples for the new Jpp v13 DAQ files (more blobs)

0.2.15 / 2020-11-06
~~~~~~~~~~~~~~~~~~~
* Add samples for the new Jpp v13 DAQ files

0.2.14 / 2020-10-27
~~~~~~~~~~~~~~~~~~~
* Fix mixed up galactic coordinates in ANTARES coordinate benchmark

0.2.13 / 2020-10-15
~~~~~~~~~~~~~~~~~~~
* More HDF5 test samples (also from ANTARES)

0.2.12 / 2020-10-15
~~~~~~~~~~~~~~~~~~~
* detx for ``offline/km3net_offline.root`` added in ``detx/km3net_offline.detx``
* numuCC (KM3) EVT file added in ``evt/``

0.2.11 / 2020-10-12
~~~~~~~~~~~~~~~~~~~
* gibuu files added in ``gibuu/``
* corant files added in ``evt/``

0.2.10 / 2020-10-06
~~~~~~~~~~~~~~~~~~~
* Added a sample file for mixed reco types

0.2.6 / 2020-09-22
~~~~~~~~~~~~~~~~~~
* Remove template artifacts
* Add Python 2.7 compatibility

0.1.0 / 2020-07-17
~~~~~~~~~~~~~~~~~~
* Project generated using the cookiecutter template from
  https://git.km3net.de/templates/python-project
