% [ str_avas, szes, lens, rast, starts ] = findAvas(asdf, binsize, varargin)
%
% Returns :
%    str_avas - a cell array containing all avalanches
%    szes - the size of each avalanche in number of spikes
%    lens - the duration of each avalanch
%    rast - a spike raster in row major ordering over the time range
%    specified, if that was specified
%    starts - times when avalanches begin
%
% Required args:
%    asdf - spike trains to find avalanches in, in another spike data
%    format (asdf)
%    binsize - the time bin to use for finding avalanches
%
% Optional args:
%     Example: [...] = findAvas(asdf, binsize, 'offset', a, 'range', b);
%     Finds avalanches only in a specified region of the raster between
%     times (in binsize) a and a+b (both inclusive)
%
%     Example: [...] = findAvas(asdf, binsize, 'threshold', theta);
%     Avalanches are defined as periods of activity greater than some
%     threshold, by default it is mean activity in each time bin/2, but
%     this can be set manually and this is how
%
%     Arguments can be entered in any order so long as argument name
%     preceeds argument.

function [ str_avas, szes, lens, rast, starts ] = findAvas( asdf, binsize, varargin)
%tic;
narginchk(2, 12);

% Defaults...
% range needs size of rast first...
customThresh = false;
td = binsize;
% assign values if specified
for i=1:2:length(varargin)
    switch varargin{i}
        case 'threshold'
            thresh = varargin{i+1};
            customThresh = true;
        case 'time difference'
            td = varargin{i+1};
    end
end

% operations are optimized when the raster is a sparse matrix such that
% each column represents a time bin since str_avas requires us to take sub
% matrices of the raster from one time index to another. See CSC sparse
% data format for why this is the case...
rast=ASDFToRaster(asdf, 'row');

% find number of spikes in each time bin
pop_fir = full(sum(rast)); # Sum of each columns
if ~customThresh
    thresh = mean(nonzeros(pop_fir))/2;
end
% put 1s where a time bin is within a valid avalache, 0 otherwise
evts = pop_fir>thresh;

% pad and find where avalanches start or end based on where 0s change to
% 1s and vice versa
act_change = diff([0 evts 0]);

% 1s indicate an avalanche began in the given time bin
starts = find(act_change == 1);
% -1s indicate an avalanche ended in the previous time bin
ends = find(act_change== -1) - 1;

if (td ~= binsize) 
    ed2 = ends(1:end-1);
    st2 = starts(2:end);

    q = st2-ed2;

    inds = 1:length(st2);
    inds = inds(q<=td);

    starts = starts([1 inds+1]);
    ends = ends([inds length(ends)]);
end

% durations...
lens = ends-starts+1;
str_avas = cell(length(lens), 1);
szes = zeros(size(lens));

for ii=1:length(lens)
    % select sub arrays of valid avalanches
    str_avas{ii} = rast(:,starts(ii):ends(ii));
    % find the number of spikes in each valid avalanche
    szes(ii) = nnz(str_avas{ii});
end

%toc;
end

