# FRB search and Classification pipieline 

This pipeline is one stop solution for searching and classifying FRB bursts in your telescope filterbank data.

This pipeline uses [PRESTO](https://github.com/scottransom/presto) for the pre-processing of the filterbank data like. dedispersion and singlepulse search 

For clustring we are using HDBSCAN

And for candidate creation we are using a modified version of [your](https://github.com/thepetabyteproject/your.git), [your-NB](https://github.com/Ankit-astro/your-NB.git) that zooms on the DM-time plot for batter classification.

And for candidate classification we are using our own trained model of [FETCH](https://github.com/devanshkv/fetch.git), that are capable of identifying narrwoband bursts [fetch-NB](https://github.com/Ankit-astro/fetch-NB.git)

