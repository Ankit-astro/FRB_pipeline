# FRB search and Classification pipeline 

This pipeline is one stop solution for searching and classifying FRB bursts in your telescope filterbank data.

This pipeline uses [PRESTO](https://github.com/scottransom/presto) for the pre-processing of the filterbank data like dedispersion and singlepulse search.

For clustering we are using HDBSCAN

And for candidate creation we are using a modified version of [your](https://github.com/thepetabyteproject/your.git), [your-NB](https://github.com/Ankit-astro/your-NB.git) that zooms on the DM-time plot for better classification.

And for candidate classification we are using our own trained model of [FETCH](https://github.com/devanshkv/fetch.git), that are capable of identifying narrowband bursts [fetch-NB](https://github.com/Ankit-astro/fetch-NB.git)

# Dependencies
1. [PRESTO](https://github.com/scottransom/presto)
2. [your-NB](https://github.com/Ankit-astro/your-NB.git)
3. [fetch-NB](https://github.com/Ankit-astro/fetch-NB.git)


