# Summary

This example demonstrates a heatmap of correlation coefficients from an LHS (Latin hypercube) study from Dakota.  The heatmap table was produced using a plotting template in Dakota GUI.

![alt text](img/partial_correlation.png "Example plot")

# Description

After running a Dakota LHS study and producing an HDF5 dataset file, many useful datasets will be produced.  Among them are correlations between the variables and responses.  The heatmap table shown above demonstrates how the Dakota input variables (nuv\_1, nuv\_2, uuv\_1, and uuv\_2) and correlated to the Dakota output responses response\_fn\_1 and response\_fn\_2.

The cell color and the number value inside the cell both demonstrate the strength of the correlation.  Here, we have applied the "Bent Cool Warm" color scale, which uses red to indicate positive correlation, blue to indicate negative correlation, and white to indicate neither. 

# Contents

- `CorrelationCoefficientsTable-partial_correlations.plot` - the plot that demonstrates partial correlation bar charts, shown above.  The name describes both the type of plot (CorrelationCoefficientsTable) and the HDF5 dataset from which the data originated (partial\_correlations).
- `basic_lhs.h5` - The original HDF5 database file that contains the results of the Dakota study.

# How to run the example

- Open Dakota GUI.
- Import this example into your workspace.
- Double-click the CorrelationCoefficientsTable-partial_correlations.plot file to view the plot.

# How to create a new plot

- Open Dakota GUI.
- Import this example into your workspace.
- Right-click the basic_lhs.h5 file, and choose `Chartreuse > New plot template from this file`.
- Choose "Correlation Coefficients Table" from the "Select Template" dropdown.
- Click on the "Get Data" button (the folder-and-file icon) to choose an HDF5 dataset to plot.
- In the "Select Plot Data" dialog that opens, select "PARTIAL\_CORRELATIONS" from the "HDF Target Object" dropdown.  You should see the dialog locate the partial\_correlations dataset within the HDF5 hierarchy on the right side of the dialog.
- Click OK to close the dialog.
- Choose any orientation you like for the table.  You may plot variables against responses, responses against variables, variables against variables, responses against responses, or all against all.  The plot above uses "Variable-Response" orientation.
- When you're finished, click OK.
- The main Plot Window Manager dialog will appear to give you a preview of the layout of your plot.  There is no further configuration necessary in this dialog, so you may click "Plot" in the bottom-right to close the dialog.
- Your new plot file should auto-open in the main editor area of Dakota GUI.

# Further Reading

- [Read in the Dakota GUI manual about other types of plots that can be produced.](https://dakota.sandia.gov/content/chartreuse-1)
- Learn about [simple correlation](https://en.wikipedia.org/wiki/Correlation_and_dependence), [rank correlation](https://en.wikipedia.org/wiki/Rank_correlation), and [partial correlation](https://en.wikipedia.org/wiki/Partial_correlation).