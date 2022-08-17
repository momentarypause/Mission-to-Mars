# Mission-to-Mars

## Purpose
In this repository is the code for a simple website that scrapes the following information from the following websites:


### https://redplanetscience.com
The first news article from this page has been scraped and dynamically placed into the target website so that an updated article will appear as the article on the original webpage changes. 

### https://spaceimages-mars.com 
The featured image from this website is scraped and placed into the target website.  This image is dynamic so the image on the target website will update as the original website changes.

### https://galaxyfacts-mars.com
The information from the planet profile has been scraped, read into a Pandas DataFrame, and placed into the target website.

### https://marshemispheres.com/
Images for all 4 of Mars' hemispheres have been scraped and placed onto the target website.


## Extras
Bootstrap 3 components were added to customize the target website.
### Mobile Friendly
There wasn't much that needed to be done to make this website mobile friendly as Bootstrap 3 has already designed it to be so.  I did change all columns from md to xs to ensure this and made the featured image responsive.
### Page Heading Container
- I extended the container to reach across the whole viewing field by adding the "container-fluid" class.
- I updated the button with the "active" class, making it appear different when pushed to allow the user visibility to know if they have pushed it to update the scraped information.  I also updated the color of the button.
### News Container Background
I updated the color of the background of this section to make it stand out as it was blending in with the rest of the information.
