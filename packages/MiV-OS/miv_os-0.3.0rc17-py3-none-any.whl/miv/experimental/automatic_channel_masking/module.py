def _auto_channel_mask_with_correlation_matrix(
    self,
    spontaneous_binned: dict[str, Any],
    filter: FilterProtocol,
    detector: SpikeDetectionProtocol,
    offset: float = 0,
    bins_per_second: float = 100,
):
    """
    Automatically apply mask.

    Parameters
    ----------
    spontaneous_binned : Iterable[Iterable[int]] | int
        [0]: 2D matrix with each column being the binned number of spikes from each channel.
        [1]: number of bins from spontaneous recording binned matrix
        [2]: array of indices of empty channels
    filter : FilterProtocol
        Filter that is applied to the signal before masking.
    detector : SpikeDetectionProtocol
        Spike detector that extracts spikes from the signals.
    offset : float, optional
        The trimmed time in seconds at the front of the signal (default = 0).
    bins_per_second : float, default=100
        Optional parameter for binning spikes with respect to time.
        The spikes are binned for comparison between the spontaneous recording and
        the other experiments. This value should be adjusted based on the firing rate.
        A high value reduces type I error; a low value reduces type II error.
        As long as this value is within a reasonable range, it should negligibly affect
        the result (see jupyter notebook demo).
    """

    exp_binned = self._get_binned_matrix(filter, detector, offset, bins_per_second)
    num_channels = np.shape(exp_binned["matrix"])[1]

    # if experiment is longer than spontaneous recording, it gets trunkated
    if exp_binned["num_bins"] > spontaneous_binned["num_bins"]:
        spontaneous_matrix = spontaneous_binned["matrix"].copy()
        exp_binned["matrix"] = exp_binned["matrix"][
            : spontaneous_binned["num_bins"] + 1
        ]

    # if spontaneous is longer than experiment recording
    elif exp_binned["num_bins"] < spontaneous_binned["num_bins"]:
        spontaneous_matrix = spontaneous_binned["matrix"].copy()
        spontaneous_matrix = spontaneous_matrix[: exp_binned["num_bins"] + 1]

    # they're the same size
    else:
        spontaneous_matrix = spontaneous_binned["matrix"].copy()

    exp_binned_channel_rows = np.transpose(exp_binned["matrix"])
    spontaneous_binned_channel_rows = np.transpose(spontaneous_matrix)

    dot_products = []
    for chan in range(num_channels):
        try:
            dot_products.append(
                np.dot(
                    spontaneous_binned_channel_rows[chan],
                    exp_binned_channel_rows[chan],
                )
            )
        except Exception:
            raise Exception(
                "Number of channels does not match between this experiment and referenced spontaneous recording."
            )

    mean = np.mean(dot_products)
    threshold = mean + np.std(dot_products)

    mask_list = []
    for chan in range(num_channels):
        if dot_products[chan] > threshold:
            mask_list.append(chan)
    self.set_channel_mask(np.concatenate((mask_list, exp_binned["empty_channels"])))


def _get_binned_matrix(
    self,
    filter: FilterProtocol,
    detector: SpikeDetectionProtocol,
    offset: float = 0,
    bins_per_second: float = 100,
) -> dict[str, Any]:
    """
    Performs spike detection and return a binned 2D matrix with columns being the
    binned number of spikes from each channel.

    Parameters
    ----------
    filter : FilterProtocol
        Filter that is applied to the signal before masking.
    detector : SpikeDetectionProtocol
        Spike detector that extracts spikes from the signals.
    offset : float, optional
        The time in seconds to be trimmed in front (default = 0).
    bins_per_second : float, default=100
        Optional parameter for binning spikes with respect to time.
        The spikes are binned for comparison between the spontaneous recording and
        the other experiments. This value should be adjusted based on the firing rate.
        A high value reduces type I error; a low value reduces type II error.
        As long as this value is within a reasonable range, it should negligibly affect
        the result (see jupyter notebook demo).

    Returns
    -------
    matrix :
        2D list with columns as channels.
    num_bins : int
        The number of bins.
    empty_channels : list[int]
        List of indices of empty channels
    """

    result = []
    for sig, times, samp in self.load(num_fragments=1):
        start_time = times[0] + offset
        starting_index = int(offset * samp)

        trimmed_signal = sig[starting_index:]
        trimmed_times = times[starting_index:]

        filtered_sig = filter(trimmed_signal, samp)
        spiketrains = detector(filtered_sig, trimmed_times, samp)

        bins_array = np.arange(
            start=start_time, stop=trimmed_times[-1], step=1 / bins_per_second
        )
        num_bins = len(bins_array)
        num_channels = len(spiketrains)
        empty_channels = []

        for chan in range(num_channels):
            if len(spiketrains[chan]) == 0:
                empty_channels.append(chan)

            spike_counts = np.zeros(shape=num_bins + 1, dtype=int)
            digitized_indices = np.digitize(spiketrains[chan], bins_array)
            for bin_index in digitized_indices:
                spike_counts[bin_index] += 1
            result.append(spike_counts)

    return {
        "matrix": np.transpose(result),
        "num_bins": num_bins,
        "empty_channels": empty_channels,
    }


def auto_channel_mask_with_firing_rate(
    self,
    filter: FilterProtocol,
    detector: SpikeDetectionProtocol,
    no_spike_threshold: float = 1,
):
    """
    Perform automatic channel masking.
    This method simply applies a Butterworth filter, extract spikes, and filter out
    the channels that contain either no spikes or too many spikes.

    Parameters
    ----------
    filter : FilterProtocol
        Filter that is applied to the signals before detecting spikes.
    detector : SpikeDetectionProtocol
        Spike detector that is used to extract spikes from the filtered signal.
    no_spike_threshold : float, default=1
        Spike rate threshold (spike per sec) for filtering channels with no spikes.
        (default = 1)

    """

    for data in self.data_list:
        for sig, times, samp in data.load(num_fragments=1):
            mask_list = []

            filtered_signal = filter(sig, samp)
            spiketrains = detector(filtered_signal, times, samp)
            spike_stats = firing_rates(spiketrains)

            for idx, channel_rate in enumerate(spike_stats["rates"]):
                if int(channel_rate) <= no_spike_threshold:
                    mask_list.append(idx)

            data.set_channel_mask(mask_list)


def auto_channel_mask_with_correlation_matrix(
    self,
    spontaneous_data: DataProtocol,
    filter: FilterProtocol,
    detector: SpikeDetectionProtocol,
    omit_experiments: Iterable[int] | None = None,
    spontaneous_offset: float = 0,
    exp_offsets: Iterable[float] | None = None,
    bins_per_second: float = 100,
):
    """
    This masking method uses a correlation matrix between a spontaneous recording and
    the experiment recordings to decide which channels to mask out.

    Notes
    -----
        Sample rate and number of channels for all recordings must be the same

    Parameters
    ----------
    spontaneous_data : Data
        Data from spontaneous recording that is used for comparison.
    filter : FilterProtocol
        Filter that is applied to the signals before detecting spikes.
    detector : SpikeDetectionProtocol
        Spike detector that is used to extract spikes from the filtered signal.
    omit_experiments: Optional[Iterable[int]]
        Integer array of experiment indices (0-based) to omit.
    spontaneous_offset: float, optional
        Postive time offset for the spontaneous experiment (default = 0).
        A negative value will be converted to 0.
    exp_offsets: Optional[Iterable[float]]
        Positive float array of time offsets for each experiment (default = 0).
        Negative values will be converted to 0.
    bins_per_second : float, default=100
        Optional parameter for binning spikes with respect to time.
        The spikes are binned for comparison between the spontaneous recording and
        the other experiments. This value should be adjusted based on the firing rate.
        A high value reduces type I error; a low value reduces type II error.
        As long as this value is within a reasonable range, it should negligibly affect
        the result (see jupyter notebook demo).
    """

    omit_experiments_list: list[float] = (
        list(omit_experiments) if omit_experiments else []
    )
    exp_offsets_list: list[float] = list(exp_offsets) if exp_offsets else []

    if spontaneous_offset < 0:
        spontaneous_offset = 0

    exp_offsets_length = sum(1 for e in exp_offsets_list)
    for i in range(exp_offsets_length):
        if exp_offsets_list[i] < 0:
            exp_offsets_list[i] = 0

    if exp_offsets_length < len(self.data_list):
        exp_offsets_list = np.concatenate(
            (
                np.array(exp_offsets_list),
                np.zeros(len(self.data_list) - exp_offsets_length),
            )
        )

    spontaneous_binned = spontaneous_data._get_binned_matrix(
        filter, detector, spontaneous_offset, bins_per_second
    )

    for exp_index, data in enumerate(self.data_list):
        if not (exp_index in omit_experiments_list):
            data._auto_channel_mask_with_correlation_matrix(
                spontaneous_binned,
                filter,
                detector,
                exp_offsets_list[exp_index],
                bins_per_second,
            )
