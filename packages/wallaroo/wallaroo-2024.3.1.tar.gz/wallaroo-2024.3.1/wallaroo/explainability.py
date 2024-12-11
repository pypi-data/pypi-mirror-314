from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)
from uuid import UUID

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import norm

from wallaroo.unwrap import unwrap

NDArray = np.ndarray

REF_MEAN_ABS = "ref_mean_abs"
REF_MAX_ABS = "ref_max_abs"
WINDOW_MEAN_ABS = "window_mean_abs"
WINDOW_MAX_ABS = "window_max_abs"


# To keep colors consistent across plots explicitly list the ones we use.
colors = [
    "red",
    "green",
    "blue",
    "gold",
    "fuchsia",
    "tan",
    "yellowgreen",
    "darkkhaki",
    "brown",
    "azure",
    "darkorchid",
    "darkslategrey",
    "moccasin",
    "sandybrown",
    "aquamarine",
    "springgreen",
    "sienna",
    "cyan",
    "mediumpurple",
    "midnightblue",
    "plum",
    "deeppink",
    "crimson",
    "lightgoldenrodyellow",
    "lightgreen",
    "lawngreen",
    "bisque",
    "steelblue",
    "cornflowerblue",
    "lightblue",
    "darksalmon",
    "lightslategrey",
]


def truncate(v: Any, num_char: int = 256) -> str:
    s = str(v)
    if len(s) < num_char:
        return s
    else:
        postfix = " ..."
        return f"{s[:num_char - len(postfix)]}{postfix}"


@dataclass
class WindowRequestInput:
    start: Optional[str]  # These are strings in our request but
    end: Optional[str]  # should be interpreted as 3339 formated datetimes
    num_samples: Optional[int]


class ExplainabilityConfigList(list):
    def _repr_html_(self):
        rows = [
            f"""
        <tr">
            <td>{exp_config.id}</td>
            <td>{exp_config.status}</td>
        </tr>
        """
            for exp_config in self
        ]
        table = """<table>
            <tr>
                <th>Id</th>
                <th>Status</th>
            </tr>
            {0}
        </table>""".format("\n".join(rows))

        return table


class ExplainabilityRequestList(list):
    """Adds a _repr_html_ to a list of explainability requests."""

    def _repr_html_(self):
        """Assuming all items are explainabilty requests generates an HTML
        table for jupyter."""
        rows = [
            f"""
        <tr">
            <td>{exp_req.id}</td>
            <td>{exp_req.status}</td>
            <td>{exp_req.reference_config}</td>
            <td>{exp_req.window_config}</td>
            <td>{exp_req.use_adhoc_data}</td>
        </tr>
        """
            for exp_req in self
        ]
        table = """<table>
            <tr>
                <th>Id</th>
                <th>Status</th>
                <th>Reference Data</th>
                <th>Window Data</th>
                <th>Adhoc</th>
            </tr>
            {0}
        </table>""".format("\n".join(rows))

        return table


@dataclass
class FeatureBounds:
    min: float
    max: float
    xs: List[float]


@dataclass
class ExplainabilityConfig:
    """This class specifies an explainability configuration that can be used
    to later submit explainability requests which cause the server to do the
    analysis and create explainability results.

    ExplainabilityConfig are necessary to ensure the explainability pipeline
    is created and is deployed and so that various requests are processed in
    the same manner and can be compared.

    id, status, feature_bounds and reference_pipeline_version are optional
    and will be filled out when processed and saved to the database.

    workspace id must match the users/pipelines workspace and
    reference_pipeline_version must refer to a valid pipeline version that the
    user has access too.

    num_points specifies how many samples to take when varying the values of a
    feature for the PDP/ICE analysis through the feature_bounds.

    feature_names are convinince for the user. output_names is not currently used.
    """

    id: Optional[UUID]
    workspace_id: int
    status: Optional[Dict[str, Any]]
    reference_pipeline_version: str
    explainability_pipeline_version: Optional[str]
    num_points: int = 10
    feature_names: Optional[List[str]] = None
    feature_bounds: Optional[Dict[str, FeatureBounds]] = None
    output_names: Optional[List[str]] = None

    def _repr_html_(self):
        fields = [
            f"<tr><td>{k}</td><td>{truncate(v)}</td></tr>"
            for k, v in asdict(self).items()
        ]
        return f"<table><tr><th>Field</th><th>Value</th></tr>{''.join(fields)}</table>"

    def list_explainability_requests(self) -> List["ExplainabilityRequest"]:
        """List the explainability requests we've created."""

        client = self.client  # type: ignore
        result = client._post_rest_api_json(
            "v1/api/explainability/list_requests",
            {"explainability_config_id": self.id},
        )
        erl = [ExplainabilityRequest(**ec) for ec in result]
        for er in erl:
            er.client = client  # type: ignore
        return ExplainabilityRequestList(erl)

    def get_explainability_request(
        self, expr: Union[str, "ExplainabilityConfig"]
    ) -> Optional["ExplainabilityRequest"]:
        """Get the full explainability result whether completed or not."""

        if isinstance(expr, str):
            explain_id = expr
        else:
            explain_id = str(expr.id)

        client = self.client  # type: ignore
        result = client._post_rest_api_json(
            "v1/api/explainability/get_request",
            {"explainability_request_id": explain_id},
        )

        exp_cfg = ExplainabilityRequest(**result)
        exp_cfg.client = client  # type: ignore
        return exp_cfg

    def submit_explainability_request(
        self,
        reference_start: Optional[datetime] = None,
        reference_end: Optional[datetime] = None,
        reference_num_samples: Optional[int] = None,
        use_reference: Optional[bool] = True,
        window_start: Optional[datetime] = None,
        window_end: Optional[datetime] = None,
        window_num_samples: Optional[int] = None,
        adhoc_data: Optional[Union[List[List[float]], np.ndarray, pd.DataFrame]] = None,
    ):
        """Submit an analysis on reference or adhoc data using a particular config"""

        reference_config = None
        if use_reference:
            reference_config = WindowRequestInput(
                start=maybe_format_date(reference_start),
                end=maybe_format_date(reference_end),
                num_samples=reference_num_samples,
            )

        window_config = None
        if window_start or window_end or window_num_samples:
            window_config = WindowRequestInput(
                start=maybe_format_date(window_start),
                end=maybe_format_date(window_end),
                num_samples=window_num_samples,
            )

        use_adhoc_data = False
        if adhoc_data is not None:
            use_adhoc_data = True

        adhoc_data_list = None
        if use_adhoc_data:
            if isinstance(adhoc_data, list):
                adhoc_data_list = adhoc_data
            elif isinstance(adhoc_data, np.ndarray):
                adhoc_data_list = adhoc_data.tolist()
            elif isinstance(adhoc_data, pd.DataFrame):
                adhoc_data_list = adhoc_data.values.tolist()
            else:
                raise Exception(f"Unknown adhoc data type {type(adhoc_data)}")

        if reference_config is None and window_config is None and not use_adhoc_data:
            raise Exception(
                "You must specify a reference config, a window config or adhoc data"
            )

        client = self.client  # type: ignore
        exp_config_id = self.id
        workspace_id = client.get_current_workspace().id()

        ear = ExplainabilityRequest(
            id=None,
            explainability_config_id=exp_config_id,
            workspace_id=workspace_id,
            reference_config=reference_config,
            window_config=window_config,
            use_adhoc_data=use_adhoc_data,
            adhoc_data=adhoc_data_list,
        )

        result = client._post_rest_api_json(
            "v1/api/explainability/create_request", asdict(ear)
        )
        expr_id = result["id"]
        return self.get_explainability_request(expr_id)


def maybe_format_date(d: Optional[datetime]) -> Optional[str]:
    if d:
        return d.astimezone(tz=timezone.utc).isoformat()
    return None


@dataclass
class ExplainabilityRequest:
    """This class outlines what should be submitted to start the explainability
    analysis with a particular config.

    The request can be to analyze reference data, historical data from the ref
    pipeline, or new adhoc data submitted with the request or both.

    id and status are optional and are filled in by the processing steps.

    If the request has use_reference_data = True, num_sample inference logs are
    sampled from between the start and end dates or the entire (last 100_000)
    inferences.
    """

    id: Optional[UUID]
    workspace_id: int
    explainability_config_id: Optional[UUID] = None
    status: Optional[Dict[str, Any]] = None
    reference_config: Optional[WindowRequestInput] = None
    window_config: Optional[WindowRequestInput] = None
    use_adhoc_data: bool = False
    adhoc_data: Optional[List[List[float]]] = None

    def _repr_html_(self):
        fields = [f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in asdict(self).items()]
        return f"<table><tr><th>Field</th><th>Value</th></tr>{''.join(fields)}</table>"

    def get_explainability_result(self) -> Optional["ExplainabilityResult"]:
        """Get the full explainability result whether completed or not."""

        client = self.client  # type: ignore

        result = client._post_rest_api_json(
            "v1/api/explainability/get_result",
            {"explainability_result_id": self.id},
        )
        return build_explainability_result(result)


@dataclass
class PDPResult:
    """This class holds the PDP/ICE part of the results.
    PDP/ICE results are generated for each observation by holding
    all but one feature constant, varying that feature and analyzing
    that prediction. Thus the results are per inference per feature.

    feature_name is the feature that this result is for.
    xs is the list of x values that the feature was varied through.

    pdp_vals is the list of resulting values.
    model, shap and feature expected values are the mean/expected values
    for that model, shap and feature.
    """

    feature_name: str
    ice_vals: np.ndarray
    pdp_vals: List[float]
    model_expected_value: List[float]
    shap_expected_value: List[float]
    feature_expected_value: List[float]


@dataclass
class WindowResult:
    data: NDArray  # the original data used for the analysis
    shap_values: NDArray  # the caculated shap values
    base_values: NDArray  # The expected value (mean) for each prediction.
    pdp_results: List[PDPResult]  # Partial dependence plot data for each feature


def find_pdp_result(window_result: WindowResult, feature_name: str) -> PDPResult:
    """Gets the pdp result object for the specified feature."""

    for p in window_result.pdp_results:
        if p.feature_name == feature_name:
            return p
    raise Exception(f"Did not find feature {feature_name} in pdp_results.")


@dataclass
class ExplainabilityResult:
    """This class holds the explainability result created by processing an
    explainability request.

    id and status are optional and will be filled in by processing. The id
    will be the same as the request id since the results are stored in minio.

    num_inferences and num_batches are nice to know status information and
    could be brought into the status object in the future.

    reference and adhoc data are the actual inferences used in the analysis.

    reference and adhoc shap values are the shap values for each feature for
    each prediction.

    base_values are the expected value for each prediction. These values will
    all be the same so may be changed to a single float in the future.

    pdp results are a list of pdp/ice results for each feature.

    """

    id: Optional[UUID]
    workspace_id: int
    explainability_config_id: UUID
    num_inferences: int
    num_batches: int
    compute_time: float
    status: Dict[str, Any]
    feature_names: List[str]  # The names of the columns
    feature_bounds: Dict[str, FeatureBounds]
    reference_result: Optional[WindowResult]
    window_result: Optional[WindowResult]
    adhoc_result: Optional[WindowResult]

    reference_color = np.array([127.0, 196, 252]) / 255
    window_color = np.array([252, 127.0, 196]) / 255

    def _repr_html_(self):
        fields = [
            f"<tr><td>{k}</td><td>{truncate(v)}</td></tr>"
            for k, v in asdict(self).items()
        ]
        return f"<table><tr><th>Field</th><th>Value</th></tr>{''.join(fields)}</table>"

    def feature_effects(self) -> pd.DataFrame:
        """Returns a dataframe summarizing the mean feature effects of the reference
        data as well as the feature effects for each adhoc inference."""

        df = pd.DataFrame(index=self.feature_names)

        if self.reference_result is not None:
            vals = np.array(self.reference_result.shap_values)
            if vals.shape[0] > 0:
                df[REF_MEAN_ABS] = np.abs(vals).mean(axis=0)
                df["ref_std_dev"] = vals.std(axis=0)
                df[REF_MAX_ABS] = np.abs(vals).max(axis=0)

        if self.window_result is not None:
            vals = np.array(self.window_result.shap_values)
            if vals.shape[0] > 0:
                df[WINDOW_MEAN_ABS] = np.abs(vals).mean(axis=0)
                df["window_std_dev"] = vals.std(axis=0)
                df[WINDOW_MAX_ABS] = np.abs(vals).max(axis=0)

        if self.adhoc_result is not None:
            vals = np.array(self.adhoc_result.shap_values)
            if vals.shape[0] > 0:
                for idx in range(vals.shape[0]):
                    df[f"input_{idx+1}"] = vals[idx, :]

        if REF_MEAN_ABS in df.columns:
            return df.sort_values(by=REF_MEAN_ABS, ascending=False)
        return df

    def effect_summary(self) -> pd.DataFrame:
        """Returns a dataframe with the expected/mean values and the shap adjustments."""

        effects = self.feature_effects()
        base_value = unwrap(self.reference_result).base_values[0]
        data = {}
        data["base_value"] = [0, base_value]

        # we should rename inputs_X to 'house_X' or similar
        input_cols = [c for c in effects.columns if "input_" in c]
        effect_sums = effects[input_cols].sum(axis=0)
        for c, v in zip(input_cols, effect_sums):
            data[c] = [v, v + base_value]
        return pd.DataFrame(data, index=["adjustment", "total"])

    def check_status(self) -> bool:
        """Ensure we've completed before trying to plot anything."""

        if self.status["status"] != "COMPLETED":
            raise Exception(f"Analysis has not (yet) completed: {self.status}")
        return True

    def plot_feature_effects(
        self,
        mode: str = "mean",
        top_n=0,
        plot_reference=True,
        plot_window=True,
        plot_adhoc=True,
    ):
        """Creates a bar plot of the mean or max abs feature effects."""

        if mode not in ["mean", "max", "individual"]:
            raise Exception("Mode must be one of: 'mean', 'max', 'individual'")

        self.check_status()

        df = self.feature_effects()
        if top_n > 0:
            df = df.head(top_n)

        cols = df.columns
        if not plot_reference:
            cols = [c for c in cols if not c.startswith("ref_")]
        if not plot_window:
            cols = [c for c in cols if not c.startswith("window_")]
        if not plot_adhoc:
            cols = [c for c in cols if c.startswith("ref_") or c.startswith("window_")]

        df = df[cols]

        if REF_MEAN_ABS in df.columns and mode != "individual":
            if mode == "max":
                title = "Max Absolute Feature Effect"
                _ = plt.bar(df.index, df[REF_MAX_ABS])
            else:
                title = "Mean Absolute Feature Effect"
                _ = plt.bar(df.index, df[REF_MEAN_ABS])
        else:
            title = "Feature Effects"
            ax = plt.subplot(1, 1, 1)
            _ = df.drop(
                ["ref_std_dev", "window_std_dev"], axis=1, errors="ignore"
            ).plot(kind="bar", ax=ax)
            plt.legend(bbox_to_anchor=(1, 1), loc="upper left")

        plt.grid()
        plt.xticks(rotation=90)
        plt.title(title)

    def plot_ice_values(
        self, feature_name: str, plot_reference=True, plot_window=True, plot_adhoc=True
    ):
        """Creates a combination ICE plot for the adhoc data if any
        in custom colors and the reference data if any in translucent
        blue."""

        self.check_status()

        ice_alpha = 0.2
        ice_width = 5

        xs = self.feature_bounds[feature_name].xs

        # pdp_result = unwrap(self.pdp_result(feature_name))
        # xs = pdp_result.xs
        # mean_vals = np.array(pdp_result.pdp_vals)
        # ice_vals = np.array(pdp_result.ice_vals)

        plt.title(f"ICE for {feature_name}")
        plt.xlabel(feature_name)
        plt.ylabel("Prediction")

        if plot_reference and self.reference_result is not None:
            pdp_result = find_pdp_result(self.reference_result, feature_name)
            ice_vals = pdp_result.ice_vals
            mean_vals = pdp_result.pdp_vals
            _ = plt.plot(
                xs,
                ice_vals,
                color=self.reference_color,
                alpha=ice_alpha,
                linewidth=ice_width,
            )
            _ = plt.plot(
                xs, mean_vals, color="black", zorder=10, label="Reference Mean"
            )

        if plot_window and self.window_result is not None:
            pdp_result = find_pdp_result(self.window_result, feature_name)
            ice_vals = pdp_result.ice_vals
            mean_vals = pdp_result.pdp_vals
            _ = plt.plot(
                xs,
                ice_vals,
                color=self.window_color,
                alpha=ice_alpha,
                linewidth=ice_width,
            )
            _ = plt.plot(
                xs, mean_vals, linestyle="dashed", color="black", label="Window Mean"
            )

        if plot_adhoc and self.adhoc_result is not None:
            pdp_result = find_pdp_result(self.adhoc_result, feature_name)
            ice_vals = np.array(pdp_result.ice_vals)
            mean_vals = pdp_result.pdp_vals
            for idx in range(self.adhoc_result.data.shape[0]):
                _ = plt.plot(
                    xs,
                    ice_vals[:, idx : idx + 1],
                    linewidth=3,
                    label=f"input_{idx+1}",
                    color=colors[idx % len(colors)],
                )
            plt.legend()

        plt.ylim(0)
        _ = plt.grid()
        plt.show()

    def plot_all_features(
        self,
        title="Feature Effect per Inference",
        plot_reference=True,
        plot_window=True,
        plot_adhoc=True,
        top_n: int = 0,
    ):
        """Creates a 'bee swarm' plot of all/each feature effect."""
        self.check_status()
        np.random.seed(42)

        # Our custom palette will go from black to a weird blue green.
        # Not sure of the best palette to use. We need lighter to be
        # higher values. Started with a red to green ramp but we also
        # need to be aware to color blindness issues.
        rgb = [(0.10, 0.10, 0.10), (0.0, 0.90, 0.90)]

        # Gather the data we'll need
        shap_values_list = []
        feature_values_list = []
        if plot_reference and self.reference_result:
            shap_values_list.append(self.reference_result.shap_values)
            feature_values_list.append(self.reference_result.data)
        if plot_window and self.window_result:
            shap_values_list.append(self.window_result.shap_values)
            feature_values_list.append(self.window_result.data)
        if plot_adhoc and self.adhoc_result:
            shap_values_list.append(self.adhoc_result.shap_values)
            feature_values_list.append(self.adhoc_result.data)

        if not shap_values_list:
            raise Exception("Some data must be specified to create a plot.")

        shap_values = np.vstack(shap_values_list)
        feature_values = np.vstack(feature_values_list)

        # create a df of the shap values / contributions
        df = pd.DataFrame(shap_values)
        df.columns = self.feature_names
        # create a df of the original feature values
        feature_df = pd.DataFrame(feature_values)
        feature_df.columns = self.feature_names

        # We plot in strips from the bottom so put the most important at the top.
        # first taking the top_n if specified.
        feature_names = list(self.feature_effects().index)
        if top_n > 0:
            feature_names = feature_names[:top_n]
        feature_names = list(reversed(feature_names))

        num_features = len(feature_names)
        num_obs = df.shape[0]

        fig = plt.figure()
        fig.patch.set_facecolor("white")
        ax = fig.get_axes()

        for i, col in enumerate(feature_names):
            # create a temp df where the y is the level + jitter
            dfc = pd.DataFrame(df[col])
            dfc["y"] = i + 1 + norm.rvs(loc=0, scale=0.1, size=num_obs)
            # vals is the original feature values and we create a custom palette
            dfc["vals"] = feature_df[col]
            unique_vals = dfc["vals"].unique()
            n_colors = len(unique_vals)
            palette = sns.blend_palette(rgb, n_colors=n_colors)

            # plot a scatter plot strip
            ax = sns.scatterplot(
                x=col,
                y="y",
                data=dfc,
                alpha=0.75,
                hue="vals",
                palette=palette,
                legend=None,
            )

        # change the tick labels from strip number to feature name
        ax.set_yticks(range(num_features + 1))
        ticks = [""]
        ticks.extend(feature_names)
        ax.set_yticklabels(ticks)

        plt.xlabel("Shap Value")
        plt.ylabel("")
        plt.title(title)
        plt.ylim(0, num_features + 1)
        plt.grid()
        plt.show()

    def plot_feature_values_vs_shap_values(
        self, feature_name: str, plot_reference=True, plot_window=True, plot_adhoc=True
    ):
        """Creates a scatter plot of the feature vs shap values.
        adhoc data if any is in custom colors. reference data in translucent
        blue."""

        self.check_status()

        alpha = 0.5

        i = self.feature_names.index(feature_name)

        plt.title(f"Shap Values for {feature_name} for Each Input")
        plt.xlabel(feature_name)
        plt.ylabel("Shap Values")
        plt.grid()

        if plot_reference and self.reference_result:
            _ = plt.scatter(
                self.reference_result.data[:, i],
                self.reference_result.shap_values[:, i],
                s=100,
                alpha=alpha,
                color=self.reference_color,
                label="Reference",
            )

        if plot_window and self.window_result:
            _ = plt.scatter(
                self.window_result.data[:, i],
                self.window_result.shap_values[:, i],
                marker="p",
                s=100,
                alpha=alpha,
                color=self.window_color,
                label="Window",
            )

        if plot_adhoc and self.adhoc_result:
            for idx in range(self.adhoc_result.data.shape[0]):
                _ = plt.scatter(
                    self.adhoc_result.data[idx, i],
                    self.adhoc_result.shap_values[idx, i],
                    marker="d",  # type: ignore
                    s=200,
                    label=f"input_{idx+1}",
                    color=colors[idx % len(colors)],
                )

        # expected_shap_values = (
        #     reference_shap_values
        #     if self.reference_result.shap_values.shape[0] > 0
        #     else adhoc_shap_values
        # )
        # expected_x = reference_x if reference_x.shape[0] > 0 else adhoc_x

        # mean_feature_value = expected_x[:, i].mean()
        # min_y = expected_shap_values[:, i].min()
        # max_y = expected_shap_values[:, i].max()
        # plt.vlines(
        #     mean_feature_value,
        #     min_y,
        #     max_y,
        #     colors="gray",
        #     linestyle="dotted",
        #     label=f"Mean {feature_name}",
        # )
        plt.legend()
        plt.show()


def build_window_result(data) -> Optional[WindowResult]:
    if data is not None:
        return WindowResult(
            data=np.array(data["data"]),
            shap_values=np.array(data["shap_values"]),
            base_values=np.array(data["base_values"]),
            pdp_results=[PDPResult(**d) for d in data["pdp_results"]],
        )
    else:
        return None


def build_explainability_result(data):
    """Convinience function to parse json into the full result object
    we want."""

    return ExplainabilityResult(
        id=data["id"],
        workspace_id=data["workspace_id"],
        explainability_config_id=data["explainability_config_id"],
        num_inferences=data["num_inferences"],
        num_batches=data["num_batches"],
        compute_time=data["compute_time"],
        status=data["status"],
        feature_names=data["feature_names"],
        feature_bounds={
            k: FeatureBounds(**v) for k, v in data["feature_bounds"].items()
        },
        reference_result=build_window_result(data["reference_result"]),
        window_result=build_window_result(data["window_result"]),
        adhoc_result=build_window_result(data["adhoc_result"]),
    )
