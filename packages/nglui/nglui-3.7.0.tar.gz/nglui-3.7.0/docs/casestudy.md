# An Example Workflow

## What problem does `nglui` solve?

To answer this question, the first thing is to understand what Neuroglancer is and why it is so important.
[Neuroglancer](https://www.github.com/) is a web app for viewing large scale 3d image datasets, built by Jeremy Maitin-Shepard at Google and with an increasing amount of community support.
It works through a metaphore of **layers**, which each layer is configured to get data from some cloud source and render it in the viewer.
For example, layers that point to a location with 3d imagery will render their images and have options for things like brightness and contrast.
Layers that point to a location with segmentation data have selectable segments, organized by id, and when segments are selected they not only highlight in 3d but also show things like meshes or skeletons associated with a segment.
Annotation layers can be used to add points, lines, or other annotations to the viewer, or pull a file of annotations from a cloud source.
Collectively, Neuroglancer collects all of this information into a **state**, a JSON object that collects both the configuration of the viewer the layers that are being visualized.
With this power and flexibility, however, comes a lot of configuration and boilerplate code to set up a viewer with the right layers and options.
While Neuroglancer offers a both a GUI and a python client to help with this, data-driven workflows can be cumbersome.

`nglui` aims to solve this problem by providing a set of tools to programmatically generate Neuroglancer states from data by splitting the "rules" guiding how to build a state from the "data" that is being visualized.
It still uses the concept of layers, but provides a set of classes and functions to configure rules for each layer you want either directly or via tools like [CAVEclient](https://caveconnectome.github.io/CAVEclient/), and then functions build a state from structured dataframes.
The goal is to not only make it easy to make new states from new data, letting Neuroglancer to be used as a visualization or annotation tools as part of a data analysis workflow.

## Example: Validating a cell type classifier

To demonstrate how `nglui` can be used, we will walk through an example of the kind of workflow for which it was designed.

Let's consider a real-world example: we have a dataset of neurons from the [MICrONs project](https://www.microns-explorer.org) and we are working on a classifier to predict which cells are neurons and what are non-neuronal cells like glia based on some set of features.
We want to validate this classifier by visualizing cells in Neuroglancer with their predictions and seeing if the classifier is making reasonable predictions in three steps:

1. Generate a Neuroglancer state from our data.
2. Assess predictions in Neuroglancer
3. Import assessment data back into our analysis.

The tools in `nglui` will help us with this.
We will first use `statebuilder` to generate a Neuroglancer state with the classifier predictions as a layer and a set of tags that a user can apply to categorize the predictions.
Second, we will use `parser` to extract the tags from the state and import them back into our analysis.
Finally, we will use a segment property to share the results in a more discoverable way.

### Step 1: Generate a Neuroglancer state from our data

### Step 1.5: Assess predictions in Neuroglancer

### Step 2: Import predictions into our analysis

### Step 3: Build an explorable state with segment properties
