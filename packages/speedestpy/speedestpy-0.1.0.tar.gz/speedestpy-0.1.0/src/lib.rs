use ndarray::parallel::prelude::*;
use ndarray::prelude::*;
use numpy::ndarray::{Array2, ArrayD, ArrayViewD, ArrayViewMutD};
use numpy::{IntoPyArray, PyArrayDyn, PyArrayMethods, PyReadonlyArrayDyn};
use pyo3::{pymodule, types::PyModule, Bound, PyResult, Python};

#[pymodule]
fn speedestpy<'py>(m: &Bound<'py, PyModule>) -> PyResult<()> {
    fn add_one(mut array: ArrayViewMutD<'_, f64>, value: f64) {
        array += value;
    }

    #[pyfn(m)]
    #[pyo3(name = "add_one")]
    fn add_one_py<'py>(array: &Bound<'py, PyArrayDyn<f64>>) {
        let array = unsafe { array.as_array_mut() };
        add_one(array, 1.0);
    }

    fn pairwise_distances_raw(array: ArrayViewD<'_, f64>) -> ArrayD<f64> {
        let n = array.shape()[0];
        let mut distances = Array2::<f64>::zeros((n, n));

        for i in 0..n {
            for j in 0..n {
                let diff = &array.slice(s![i, ..]) - &array.slice(s![j, ..]);
                distances[(i, j)] = diff.dot(&diff).sqrt();
            }
        }

        distances.into_dyn()
    }

    fn pairwise_distances_ndarray(array: ArrayViewD<'_, f64>) -> ArrayD<f64> {
        let points = array
            .into_dimensionality::<Ix2>()
            .expect("Input array must be 2D");

        let n = points.shape()[0];
        let shape = IxDyn(&[n, n]);
        let diff_squared_sum = ArrayD::from_shape_fn(shape, |idx| {
            let (i, j) = (idx[0], idx[1]);
            let diff = &points.row(i) - &points.row(j);
            diff.dot(&diff)
        });

        diff_squared_sum.mapv_into(f64::sqrt)
    }

    fn pairwise_distances_rayon(array: ArrayViewD<'_, f64>) -> ArrayD<f64> {
        // Ensure the input is 2-dimensional
        let points = array
            .into_dimensionality::<Ix2>()
            .expect("Input array must be 2D");

        let n = points.shape()[0];

        let shape = IxDyn(&[n, n]);

        let distances = (0..n)
            .into_par_iter()
            .map(|i| {
                (0..n)
                    .map(|j| {
                        let diff = &points.row(i) - &points.row(j);
                        diff.dot(&diff).sqrt()
                    })
                    .collect::<Vec<f64>>()
            })
            .collect::<Vec<Vec<f64>>>()
            .into_iter()
            .flatten()
            .collect::<Vec<f64>>();

        ArrayD::from_shape_vec(shape, distances).unwrap()
    }

    fn pairwise_distances_ndarray_parralel(array: ArrayViewD<'_, f64>) -> ArrayD<f64> {
        // Ensure the input is 2-dimensional
        let points = array
            .into_dimensionality::<Ix2>()
            .expect("Input array must be 2D");

        // Extract the number of rows (points)
        let n = points.shape()[0];

        // Convert the shape to IxDyn for dynamically shaped arrays
        let shape = IxDyn(&[n, n]);

        // Create a 2D output array
        let mut distances = ArrayD::zeros(shape);

        // Parallelize row computations
        distances
            .axis_iter_mut(Axis(0))
            .into_par_iter()
            .enumerate()
            .for_each(|(i, mut row)| {
                for j in 0..n {
                    let diff = &points.row(i) - &points.row(j);
                    row[j] = diff.dot(&diff).sqrt(); // Compute distance
                }
            });

        distances
    }

    #[pyfn(m)]
    #[pyo3(name = "pairwise_distances_raw")]
    fn pairwise_distances_raw_py<'py>(
        py: Python<'py>,
        array: PyReadonlyArrayDyn<'py, f64>,
    ) -> Bound<'py, PyArrayDyn<f64>> {
        pairwise_distances_raw(array.as_array()).into_pyarray(py)
    }

    #[pyfn(m)]
    #[pyo3(name = "pairwise_distances_broadcast")]
    fn pairwise_distances_broadcast_py<'py>(
        py: Python<'py>,
        array: PyReadonlyArrayDyn<'py, f64>,
    ) -> Bound<'py, PyArrayDyn<f64>> {
        pairwise_distances_ndarray(array.as_array()).into_pyarray(py)
    }

    #[pyfn(m)]
    #[pyo3(name = "pairwise_distances_rayon")]
    fn pairwise_distances_rayon_py<'py>(
        py: Python<'py>,
        array: PyReadonlyArrayDyn<'py, f64>,
    ) -> Bound<'py, PyArrayDyn<f64>> {
        pairwise_distances_rayon(array.as_array()).into_pyarray(py)
    }

    #[pyfn(m)]
    #[pyo3(name = "pairwise_distances_ndarray_parralel")]
    fn pairwise_distances_ndarray_parralel_py<'py>(
        py: Python<'py>,
        array: PyReadonlyArrayDyn<'py, f64>,
    ) -> Bound<'py, PyArrayDyn<f64>> {
        pairwise_distances_ndarray_parralel(array.as_array()).into_pyarray(py)
    }

    Ok(())
}
