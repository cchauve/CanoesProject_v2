# Mathematical Canoes and Canoe Buoyancy
These are notebooks about First Nation canoes and the mathematics we can use to model them. This is not a piece about coding. This is about what mathematical tools we can use to create and retrieve valuable information about the Canoes.  

Users only need to import the Interface Scripts<br />
<code> import scripts.BezierCurve_Interface as bci</code><br />
<code> import scripts.BezierSurf_Interface as bsi</code><br />
<code> import scripts.Buoyancy_Interface as bi </code>

The interactive graphs are<br />
<code> bci.CurveGraph() </code>

<code> widgetLength, widgetWidth, widgetHeight, widgetNames = bsi.GetWidgets()</code><br />
<code>bsi.Canoe(widgetLength, widgetWidth, widgetHeight, widgetNames)</code><br />
<code>bi.CanoeBuoyancy(widgetLength, widgetWidth, widgetHeight, widgetNames)</code>


<code> bi.CubeGraph() </code>

## The mathematics being used

The main mathematics at play are **Bézier Curves**, they allow us to create complex shapes with simple equations. The only downside is that they require the designer to hand place key points along the canoes surface in order to define it. This almost requires you to have a 3d canoe model in order to create the canoe model. <br />
A tutorial/ designer document will be out at some point addressing this. It will detail a third party tool [Blender 3d](https://www.blender.org/) used for making a 3d model, then handplacing bezier curves along the surface to gather the correct points. 

