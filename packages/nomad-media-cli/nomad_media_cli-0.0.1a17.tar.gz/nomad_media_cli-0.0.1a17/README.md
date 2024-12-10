# Nomad Media CLI Tool

Command line interface for managing Nomad Media media assets.

## Installation

The current Nomad Media CLI is in a testing state. As such, you have to include the version # when installing.

```bash
// Fresh installation
pip install nomad-media-cli==0.0.1a17

// Upgrade
pip install --upgrade nomad-media-cli==0.0.1a17
```

## Configuration

The Nomad Media CLI stores some data locally for the SDK configuration. The location depends on the platform of your OS:

- Default config location: 
  - **Windows**: `%APPDATA%\Local\nomad_media_cli\config.json`
  - **Linux**: `~/.config/nomad_media_cli/config.json`
  - **Mac**: `~/Library/Application Support/nomad_media_cli/config.json`
- Custom config location: Use --config-path option.

## Commands

### init

Initializes CLI configuration

Options:

- `--service-api-url`: API endpoint URL (required)
- `--api-type`: API type [admin|portal]
- `--debug`: Enable debug mode [true|false]

## login

Logs into Nomad with given credentials

Options:

- `--username`: Username used for credentials. 
- `--password`: Password used for credentials.

## logout

Logs out of Nomad. Removes token, refresh token, id and expiration seconds from config.

### list-config-path

Outputs the local OS location where the config file is stored.

### update-config

Updates CLI configuration

Options:

- `--service-api-url`: API endpoint URL
- `--api-type`: API type [admin|portal]
- `--debug`: Enable debug mode [true|false]

### list-assets

List assets by id, Nomad URL or object-key. You should only specify **one **of the optional parameters.

Options:

- `--id`: Asset ID, collection id, or saved search id to list the assets for.
- `--url`: The Nomad URL of the Asset (file or folder) to list the assets for (bucket::object_key).
- `--object-key`: Object-key only of the Asset (file or folder) to list the assets for. This option assumes the default bucket that was previously set with the `set-bucket` command.

### upload-assets

Uploads a file or folder from the local OS to the Nomad asset storage. You should only specify **one **of the optional parameters for id, url or object-key. 

Options:

- `-r`: Recursive upload.
- `--source`: Local OS file or folder path specifying the files or folders to upload. For example: file.jpg or folderName/file.jpg.
- `--id`: Nomad ID of the Asset Folder to upload the source file(s) and folder(s) into.
- `--url`: The Nomad URL of the Asset folder to upload the source files/folders into (bucket::object_key).
- `--object-key`: Object-key only of the Asset folder to upload the source files/folders into. This option assumes the default bucket that was previously set with the `set-bucket` command.

### list-buckets

Lists all of the buckets registered in the Nomad instance.

### set-bucket

Sets the default bucket for use in the commands that take the object_key property. Note this must be set before using the other commands.

Options:

- `--bucket`: Name of the default bucket to set in config.

### list-tags

Lists all of the tags

Options:

- `--size`: The number of results shown. Default is 10.
- `--offset`: The offset of the page.

## add-tag-or-collection

Options:

Adds a tag or collection to an asset

- `--id`: The ID of the asset.
- `--url`: The Nomad URL of the Asset (file or folder) to add the tag/collection for (bucket::object-key).
- `--object-key`: Object-key only of the Asset (file or folder) to add the tag/collection for. This option assumes the default bucket that was previously set with the `set-bucket` command.
- `--content-definition`: The content definition.
- `--tag-name`: The name of the tag or collection.
- `--tag-id`: The ID of the tag or collection.
- `--create-new`: The create new flag.

## Future

## get-config

Options:

- `--config-type`: The type of config to get. 1 - Admin, 2 - Lambda, 3 - Groundtruth
## create-content

Options:

- `--content-definition-id`: The id of the content definition to create.
- `--language-id`: The id of the language to create the content in.
## deactivate-content-user-track

Options:

- `--session-id`: The ID of the session.
- `--content-id`: The ID of the content.
- `--content-definition-id`: The ID of the content definition.
- `--deactivate`: The deactivate flag.
## delete-content

Options:

- `--content-id`: The id of the content to delete.
## get-content

Options:

- `--content-id`: The id of the content to retrieve.
## get-content-user-track

Options:

- `--content-id`: The ID of the content.
- `--content-definition-id`: The ID of the content definition.
- `--sort_column`: The sort column.
- `--is-desc`: The is descending flag.
- `--page-index`: The page index.
- `--size-index`: The size index.

## get-content-user-track-touch

Options:

- `--content-id`: The ID of the content.
- `--content-definition-id`: The ID of the content definition.

## update-content

Options:

- `--content-id`: The ID of the content to update.
- `--content-definition-id`: The ID of the content definition the content belongs to.
- `--properties`: The properties to update in JSON dict format.
- `--language-id`: The language id of the asset to upload.

## get-content-definition

Options:

- `--content-definition-id`: The ID of the content definition to retrieve.
## get-content-definitions

Options:

- `--content-management-type`: The type of content management to get. 1; None, 2; DataSelector, 3; FormSelector
- `--sort-column`: The column to sort by.
- `--is-desc`: Whether to sort descending.
- `--page-index`: The page index to get.
- `--page-size`: The page size to get.
## update-content-definition

Options:

- `--content-definition-id`: The ID of the content definition to update.
- `--name`: The name of the content definition.
- `--content-fields`: The content fields of the content definition in JSON list format.
- `--content-definition-group`: The content definition group of the content definition.
- `--content-definition-type`: The content definition type of the content definition.
- `--display-field`: The display field of the content definition.
- `--route-item-name-field`: The name of the route item.
- `--security-groups`: The security group(s
- `--system-roles`: The system roles of the content definition. Multiple flags for multiple system roles.
- `--include-in-tags`: Whether to include the content definition in tags.
- `--index-content`: Whether to index the content.
## add-live-schedule-to-event

Options:

- `--event-id`: The ID of the event to add the live schedule to.
- `--slate-video`: The slate video ID of the event in JSON dict format.
- `--preroll-video`: The preroll video of the event in JSON dict format.
- `--postroll-video`: The postroll video of the event in JSON dict format.
- `--is-secure-output`: Whether the event is secure output.
- `--archive-folder`: The archive folder of the event in JSON dict format.
- `--primary-live-input`: The live input A ID of the event in JSON dict format.
- `--backup-live-input`: The live input B ID of the event in JSON dict format.
- `--primary-livestream-input-url`: The primary live stream URL of the event.
- `--backup-livestream-input-url`: The backup live stream URL of the event.
- `--external-output-profiles`: The external output profiles of the event in JSON list format.
- `--status`: Current status of the Live Channel Settings configuration in JSON dict format.
- `--status-message`: The status message of the event.
- `--live-channel`: The live channel of the event in JSON dict format.
- `--override-settings`: Whether to override the settings of the event.
- `--output-profile-group`: The output profile group of the event in JSON dict format.
## create-update-event

Options:

- `--content-id`: The content id of the event to update. None for create.
- `--content-definition-id`: The content definition id of the event.
- `--name`: The name of the event.
- `--start-datetime`: The start date time of the event.
- `--end-datetime`: The end date time of the event.
- `--event-type`: The event type of the event in JSON dict format.
- `--series`: The series of the event in JSON dict format.
- `--is-disabled`: Whether the event is disabled.
- `--override-series-properties`: Whether to override the series properties.
- `--series-properties`: The properties of the event in JSON dict format.
## delete-event

Options:

- `--content-id`: The ID of the event to delete.
- `--content-definition-id`: The content definition ID of the event to delete.
## extent-live-schedule

Options:

- `--event-id`: The ID of the event to extend the live schedule of.
- `--recurring-days`: The days of the week to extend the live schedule of in JSON list format.
- `--recurring-weeks`: The number of weeks to extend the live schedule of.
- `--end-date`: The end date to extend the live schedule of.
## get-live-schedule

Options:

- `--event-id`: The ID of the event to get the live schedule of.
## start-live-schedule

Options:

- `--event-id`: The ID of the event to start the live schedule of.
## stop-live-schedule

Options:

- `--event-id`: The ID of the event to stop the live schedule of.
## clip-live-channel

Options:

- `--live-channel-id`: The ID of the live channel to clip.
- `--start-time-code`: The start time code of the live channel to clip.
- `--end-time-code`: The end time code of the live channel to clip.
- `--title`: The title of the live channel to clip.
- `--output-folder-id`: The output folder ID of the live channel to clip.
- `--tags`: The tags of the live channel to clip in JSON list format.
- `--collections`: The collections of the live channel to clip in JSON list format.
- `--related-contents`: The related contents of the live channel to clip in JSON list format.
- `--video-bitrate`: The video bitrate of the live channel to clip.
- `--audio-tracks`: The audio tracks of the live channel to clip in JSON list format.
## create-live-channel

Options:

- `--name`: The name of the live channel.
- `--thumbnail-image-id`: The thumbnail image ID of the live channel.
- `--archive-folder-asset-id`: The archive folder asset ID of the live channel.
- `--enable-high-availability`: Indicates if the live channel is enabled for high availability.
- `--enable-live-clipping`: Indicates if the live channel is enabled for live clipping.
- `--is-secure-output`: Indicates if the live channel is secure output.
- `--is-output-screenshot`: Indicates if the live channel is output screenshot.
- `--channel-type`: The type of the live channel. The types are External, IVS, Normal, and Realtime.
- `--external-service-api-url`: The external service API URL of the live channel. Only required if the type is External.
- `--security-groups`: The security groups of the live channel in JSON list format.
## delete-live-channel

Options:

- `--live-channel-id`: The ID of the live channel.
- `--delete-inputs`: Indicates if the live channel inputs should be deleted.
## get-live-channel

Options:

- `--live-channel-id`: The ID of the live channel.
## next-event

Options:

- `--live-channel-id`: The ID of the live channel.
## start-live-channel

Options:

- `--live-channel-id`: The ID of the live channel.
- `--wait-for-start`: Indicates if the live channel should wait for start.
## start-output-tracking

Options:

- `--live-channel-id`: The ID of the live channel.
## stop-live-channel

Options:

- `--live-channel-id`: The ID of the live channel.
- `--wait-for-stop`: Indicates if the live channel should wait for stop.
## update-live-channel

Options:

- `--live-channel-id`: The ID of the live channel.
- `--name`: The name of the live channel.
- `--thumbnail-image-id`: The thumbnail image ID of the live channel.
- `--archive-folder-asset-id`: The archive folder asset ID of the live channel.
- `--enable-high-availability`: Indicates if the live channel is enabled for high availability.
- `--enable-live-clipping`: Indicates if the live channel is enabled for live clipping.
- `--is-secure-output`: Indicates if the live channel is secure output.
- `--is-output-screenshot`: Indicates if the live channel is output screenshot.
- `--channel-type`: The type of the live channel. The types are External, IVS, Normal, and Realtime.
- `--external-service-api-url`: The external service API URL of the live channel. Only required if the type is External.
- `--security-groups`: The security groups of the live channel in JSON list format.
## create-live-input

Options:

- `--name`: The name of the live input.
- `--source`: The source of the live input.
- `--input-type`: The type of the live input. The types are RTMP_PULL, RTMP_PUSH, RTP_PUSH, UDP_PUSH and URL_PULL.
- `--is-standard`: Indicates if the live input is standard.
- `--video-asset-id`: The video asset ID of the live input.
- `--destinations`: The destinations of the live input in JSON list format.
- `--sources`: The sources of the live input in JSON list format.
## delete-live-input

Options:

- `--live-input-id`: The ID of the live input.
## get-live-input

Options:

- `--live-input-id`: The ID of the live input.
## update-live-input

Options:

- `--live-input-id`: The ID of the live input.
- `--name`: The name of the live input.
- `--source`: The source of the live input.
- `--input-type`: The type of the live input. The types are RTMP_PULL, RTMP_PUSH, RTP_PUSH, UDP_PUSH and URL_PULL.
- `--is-standard`: Indicates if the live input is standard.
- `--video-asset-id`: The video asset ID of the live input.
- `--destinations`: The destinations of the live input in JSON list format.
- `--sources`: The sources of the live input in JSON list format.
## cancel-broadcast

Options:

- `--live-operator-id`: The ID of the live operator.
## cancel-segment

Options:

- `--live-operator-id`: The ID of the live operator.
## complete-segment

Options:

- `--live-operator-id`: The ID of the live operator.
- `--related-content-ids`: The related content IDs of the live operator in JSON list format.
- `--tag-ids`: The tag IDs of the live operator in JSON list format.
## get-completed-segments

Options:

- `--live-operator-id`: The ID of the live operator.
## get-live-operator

Options:

- `--live-operator-id`: The ID of the live operator.
## start-broadcast

Options:

- `--live-operator-id`: The ID of the live operator.
- `--preroll-asset-id`: The preroll asset ID of the live operator.
- `--postroll-asset-id`: The postroll asset ID of the live operator.
- `--live-input-id`: The live input ID of the live operator.
- `--related-content-ids`: The related content IDs of the live operator in JSON list format.
- `--tag-ids`: The tag IDs of the live operator in JSON list format.
## start-segment

Options:

- `--live-operator-id`: The ID of the live operator.
## stop-broadcast

Options:

- `--live-operator-id`: The ID of the live operator.
## create-live-output-profile

Options:

- `--name`: The name of the live output profile.
- `--output-type`: The type of the live output profile in JSON dict format.
- `--enabled`: Indicates if the live output profile is enabled.
- `--audio-bitrate`: The audio bitrate of the live output profile.
- `--output-stream-key`: The output stream key of the live output profile.
- `--output-url`: The output URL of the live output profile.
- `--secondary-output-stream-key`: The secondary output stream key of the live output profile.
- `--secondary-url`: The secondary URL of the live output profile.
- `--video-bitrate`: The video bitrate of the live output profile.
- `--video-bitrate-mode`: The video bitrate mode of the live output profile. The modes are CBR and VBR.
- `--video-codec`: The video codec of the live output profile. The codecs are H264 and H265.
- `--video-frames-per-second`: The video frames per second of the live output profile.
- `--video-height`: The video height of the live output profile.
- `--video-width`: The video width of the live output profile.
## delete-live-output-profile

Options:

- `--live-output-id`: The ID of the live output profile.
## get-live-output-profile

Options:

- `--live-output-id`: The ID of the live output profile.
## update-live-output-profile

Options:

- `--live-output-id`: The ID of the live output profile.
- `--name`: The name of the live output profile.
- `--output-type`: The type of the live output profile in JSON dict format.
- `--enabled`: Indicates if the live output profile is enabled.
- `--audio-bitrate`: The audio bitrate of the live output profile.
- `--output-stream-key`: The output stream key of the live output profile.
- `--output-url`: The output URL of the live output profile.
- `--secondary-output-stream-key`: The secondary output stream key of the live output profile.
- `--secondary-url`: The secondary URL of the live output profile.
- `--video-bitrate`: The video bitrate of the live output profile.
- `--video-bitrate-mode`: The video bitrate mode of the live output profile. The modes are CBR and VBR.
- `--video-codec`: The video codec of the live output profile. The codecs are H264 and H265.
- `--video-frames-per-second`: The video frames per second of the live output profile.
- `--video-height`: The video height of the live output profile.
- `--video-width`: The video width of the live output profile.
## create-live-output-profile-group

Options:

- `--name`: The name of the live output profile group.
- `--is-enabled`: Indicates if the live output profile group is enabled.
- `--manifest-type`: The manifest type of the live output profile group. The types are HLS, DASH, and BOTH.
- `--is-default-group`: Indicates if the live output profile group is the default group.
- `--live-output-type`: The type of the live output profile group in JSON list format.
- `--archive-live-output-profile`: The archive live output profile of the live output profile group in JSON list format.
- `--live-output-profiles`: The live output profiles of the live output profile group in JSON list format.
## delete-live-output-profile-group

Options:

- `--live-output-profile-group-id`: The ID of the live output profile group.
## get-live-output-profile-group

Options:

- `--live-output-profile-group-id`: The ID of the live output profile group.
## update-live-output-profile-group

Options:

- `--live-output-profile-group-id`: The ID of the live output profile group.
- `--name`: The name of the live output profile group.
- `--is-enabled`: Indicates if the live output profile group is enabled.
- `--manifest-type`: The manifest type of the live output profile group. The types are HLS, DASH, and BOTH.
- `--is-default-group`: Indicates if the live output profile group is the default group.
- `--live-output-type`: The type of the live output profile group in JSON list format.
- `--archive-live-output-profile`: The archive live output profile of the live output profile group in JSON list format.
- `--live-output-profile`: The live output profile of the live output profile group in JSON list format.
## create-intelligent-playlist

Options:

- `--collections`: The collections of the intelligent playlist in JSON list format.
- `--end-search-date`: The end search date of the intelligent playlist. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.
- `--end-search-duration-in-minutes`: The end search duration in minutes of the intelligent playlist.
- `--name`: The name of the intelligent playlist.
- `--related-contents`: The related content of the intelligent playlist in JSON list format.
- `--search-date`: The search date of the intelligent playlist. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.
- `--search-duration-in-minutes`: The search duration in minutes of the intelligent playlist.
- `--search-filter-type`: The search filter type of the intelligent playlist. Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
- `--tags`: The tags of the intelligent playlist in JSON list format.
- `--thumbnail-asset`: The thumbnail asset of the intelligent playlist in JSON dict format.
## create-intelligent-schedule

Options:

- `--default-video-asset`: The default video asset of the intelligent schedule in JSON dict format.
- `--name`: The name of the intelligent schedule.
- `--thumbnail-asset`: The thumbnail asset of the intelligent schedule in JSON dict format.
- `--time-zone-id`: The time zone ID of the intelligent schedule.
## create-playlist

Options:

- `--name`: The name of the playlist.
- `--thumbnail-asset`: The thumbnail asset of the playlist in JSON dict format.
- `--loop-playlist`: Whether the playlist is looped.
- `--default-video-asset`: The default video asset of the playlist in JSON dict format.
## create-playlist-video

Options:

- `--playlist-id`: The ID of the playlist.
- `--video-asset`: The video asset of the playlist video in JSON dict format.
- `--previous-item`: The previous item of the playlist video.
## delete-intelligent-playlist

Options:

- `--schedule-id`: The ID of the intelligent playlist to be deleted.
## delete-intelligent-schedule

Options:

- `--schedule-id`: The ID of the intelligent schedule to be deleted.
## delete-playlist

Options:

- `--schedule-id`: The ID of the playlist to be deleted.
## delete-schedule-item

Options:

- `--schedule-id`: The ID of the schedule the schedule item is to be deleted from.
- `--item-id`: The ID of the item to be deleted.
## get-intelligent-playlist

Options:

- `--schedule-id`: The ID of the intelligent playlist to be gotten.
## get-intelligent-schedule

Options:

- `--schedule-id`: The ID of the intelligent schedule to be gotten.
## get-playlist

Options:

- `--schedule-id`: The ID of the playlist to be gotten.
## get-schedule-item

Options:

- `--schedule-id`: The ID of the schedule the schedule item is to be gotten from.
- `--item-id`: The ID of the item to be gotten.
## get-schedule-items

Options:

- `--schedule-id`: The ID of the schedule the schedule items are to be gotten from.
## get-schedule-preview

Options:

- `--schedule-id`: The ID of the schedule the schedule preview is to be gotten from.
## move-schedule-item

Options:

- `--schedule-id`: The ID of the schedule the schedule item is to be moved from.
- `--item-id`: The ID of the item to be moved.
- `--previous-item`: The previous item of the schedule item.
## publish-intelligent-schedule

Options:

- `--schedule-id`: The ID of the schedule to be published.
- `--number-of-locked-days`: The number of locked days of the intelligent schedule.
## start-schedule

Options:

- `--schedule-id`: The ID of the schedule to be started.
- `--skip-cleanup-on-failure`: Whether or not to skip cleanup on failure.
## stop-schedule

Options:

- `--schedule-id`: The ID of the schedule to be stopped.
- `--force-stop`: Whether or not to force a stop.
## update-intelligent-playlist

Options:

- `--schedule-id`: The ID of the schedule the intelligent playlist is to be updated.
- `--collections`: The collections of the intelligent playlist in JSON list format.
- `--end-search-date`: The end search date of the intelligent playlist. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.
- `--end-search-duration-in-minutes`: The end search duration in minutes of the intelligent playlist.
- `--name`: The name of the intelligent playlist.
- `--related-contents`: The related content of the intelligent playlist in JSON list format.
- `--search-date`: The search date of the intelligent playlist. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.
- `--search-duration-in-minutes`: The search duration in minutes of the intelligent playlist.
- `--search-filter-type`: The search filter type of the intelligent playlist. Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
- `--tags`: The tags of the intelligent playlist in JSON list format.
- `--thumbnail-asset`: The thumbnail asset of the intelligent playlist in JSON dict format.
## update-intelligent-schedule

Options:

- `--schedule-id`: The ID of the schedule the intelligent schedule is to be updated.
- `--default-video-asset`: The default video asset of the intelligent schedule in JSON dict format.
- `--name`: The name of the intelligent schedule.
- `--thumbnail-asset`: The thumbnail asset of the intelligent schedule in JSON dict format.
- `--time-zone-id`: The time zone ID of the intelligent schedule.
## update-playlist

Options:

- `--schedule-id`: The ID of the schedule the playlist is to be updated from.
- `--default-video-asset`: The default video asset of the playlist in JSON dict format.
- `--loop-playlist`: Whether or not to loop the playlist.
- `--name`: The name of the playlist.
- `--thumbnail-asset`: The thumbnail asset of the playlist in JSON dict format.
## update-playlist-video

Options:

- `--playlist-id`: The ID of the schedule the playlist video is to be updated from.
- `--item-id`: The ID of the item to be updated.
- `--asset`: The asset of the playlist video in JSON dict format.
## create-schedule-item-asset

Options:

- `--schedule-id`: The ID of the schedule the asset item is to be added to.
- `--asset`: The asset of the schedule item asset in JSON dict format.
- `--days`: The days of the schedule item asset in JSON list format.
- `--duration-time-code`: The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the schedule item asset. Format: hh:mm:ss;ff.
- `--previous-item`: The previous item of the schedule item asset.
- `--time-code`: The time code of the schedule item asset. Format: hh:mm:ss;ff.
## create-schedule-item-live-channel

Options:

- `--schedule-id`: The ID of the schedule the live channel item is to be added to.
- `--days`: The days of the schedule item live channel in JSON list format.
- `--duration-time-code`: The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the schedule item live channel. Format: hh:mm:ss;ff.
- `--live-channel`: The live channel of the schedule item live channel in JSON dict format.
- `--previous-item`: The previous item of the schedule item live channel.
- `--time-code`: The time code of the schedule item live channel. Format: hh:mm:ss;ff.
## create-schedule-item-playlist-schedule

Options:

- `--schedule-id`: The ID of the schedule the playlist schedule item is to be added to.
- `--days`: The days of the schedule item playlist schedule in JSON list format.
- `--duration-time-code`: The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the schedule item playlist schedule. Format: hh:mm:ss;ff.
- `--playlist-schedule`: The playlist schedule of the schedule item playlist schedule in JSON dict format.
- `--previous-item`: The previous item of the schedule item playlist schedule.
- `--time-code`: The time code of the schedule item playlist schedule. Format: hh:mm:ss;ff.
## create-schedule-item-search-filter

Options:

- `--schedule-id`: The ID of the schedule the search filter item is to be added to.
- `--collections`: The collections of the schedule item search filter in JSON list format.
- `--days`: The days of the schedule item search filter in JSON list format.
- `--duration-time-code`: The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.
- `--end-search-date`: The end search date of the schedule item search filter. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.
- `--end-search-duration-in-minutes`: The end search duration in minutes of the schedule item search filter.
- `--end-time-code`: The end time code of the schedule item search filter. Format: hh:mm:ss;ff.
- `--previous-item`: The previous item of the schedule item search filter.
- `--related-contents`: The related contents of the schedule item search filter in JSON list format.
- `--search-date`: The search date of the schedule item search filter. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.
- `--search-duration-in-minutes`: The search duration in minutes of the schedule item search filter.
- `--search-filter-type`: The search filter type of the schedule item search filter. Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
- `--tags`: The tags of the schedule item search filter in JSON list format.
- `--time-code`: The time code of the schedule item search filter. Format: hh:mm:ss;ff.
## update-schedule-item-asset

Options:

- `--schedule-id`: The ID of the schedule the schedule item asset is to be updated from.
- `--item-id`: The ID of the item to be updated.
- `--asset`: The asset of the schedule item asset in JSON dict format.
- `--days`: The days of the schedule item asset in JSON list format.
- `--duration-time-code`: The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the schedule item asset. Format: hh:mm:ss;ff.
- `--time-code`: The time code of the schedule item asset. Format: hh:mm:ss;ff.
## update-schedule-item-live-channel

Options:

- `--schedule-id`: The ID of the schedule the schedule item live channel is to be updated from.
- `--item-id`: The ID of the item to be updated.
- `--days`: The days of the schedule item live channel in JSON list format.
- `--duration-time-code`: The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the schedule item live channel. Format: hh:mm:ss;ff.
- `--live-channel`: The live channel of the schedule item live channel in JSON dict format.
- `--time-code`: The time code of the schedule item live channel. Format: hh:mm:ss;ff.
## update-schedule-item-playlist-schedule

Options:

- `--schedule-id`: The ID of the schedule the schedule item playlist schedule is to be updated from.
- `--item-id`: The ID of the item to be updated.
- `--days`: The days of the schedule item playlist schedule in JSON list format.
- `--duration-time-code`: The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the schedule item playlist schedule. Format: hh:mm:ss;ff.
- `--playlist-schedule`: The playlist schedule of the schedule item playlist schedule in JSON dict format.
- `--time-code`: The time code of the schedule item playlist schedule. Format: hh:mm:ss;ff.
## update-schedule-item-search-filter

Options:

- `--schedule-id`: The ID of the schedule the schedule item search filter is to be updated from.
- `--item-id`: The ID of the item to be updated.
- `--collections`: The collections of the schedule item search filter in JSON list format.
- `--days`: The days of the schedule item search filter in JSON list format.
- `--duration-time-code`: The duration time between time_code and end_time_code. Format: hh:mm:ss;ff.
- `--end-search-date`: The end search date of the schedule item search filter. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.
- `--end-search-duration-in-minutes`: The end search duration in minutes of the schedule item search filter.
- `--end-time-code`: The end time code of the schedule item search filter. Format: hh:mm:ss;ff.
- `--related-contents`: The related contents of the schedule item search filter in JSON list format.
- `--search-date`: The search date of the schedule item search filter. Format: yyyy-MM-dd.THH:MM:SS.FFFZ.
- `--search-duration-in-minutes`: The search duration in minutes of the schedule item search filter.
- `--search-filter-type`: The search filter type of the schedule item search filter. Values: Random: 1, Random within a Date Range: 2, Newest: 3, Newest Not Played: 4
- `--tags`: The tags of the schedule item search filter in JSON list format.
- `--time-code`: The time code of the schedule item search filter. Format: hh:mm:ss;ff.
## add-asset-schedule-event

Options:

- `--live-channel-id`: The ID of the live channel.
- `--asset`: The asset of the asset schedule event in JSON dict format.
- `--is-loop`: Indicates if the asset schedule event should loop.
- `--duration-time-code`: The duration time code of the asset schedule event. Format: hh:mm:ss;ff.
- `--previous-id`: The ID of the previous asset schedule event.
## add-input-schedule-event

Options:

- `--live-channel-id`: The ID of the live channel.
- `--live-input`: The live input of the live input schedule event in JSON dict format.
- `--backup-live-input`: The backup live input of the live input schedule event in JSON dict format.
- `--fixed-on-air-time-utc`: The fixed on air time UTC of the live input schedule event. Format: hh:mm:ss;ff.
- `--previous-id`: The ID of the previous live input schedule event.
## get-asset-schedule-event

Options:

- `--live-channel-id`: The ID of the live channel.
- `--schedule-event-id`: The ID of the schedule event.
## get-input-schedule-event

Options:

- `--live-channel-id`: The ID of the live channel.
- `--schedule-event-id`: The ID of the schedule event.
## move-schedule-event

Options:

- `--live-channel-id`: The ID of the live channel.
- `--schedule-event-id`: The ID of the schedule event.
- `--previous-schedule-event-id`: The previous schedule event ID of the schedule event.
## remove-asset-schedule-event

Options:

- `--live-channel-id`: The ID of the live channel.
- `--schedule-event-id`: The ID of the schedule event.
## remove-input-schedule-event

Options:

- `--live-channel-id`: The ID of the live channel.
- `--input-id`: The ID of the schedule event.
## update-asset-schedule-event

Options:

- `--event-id`: The ID of the schedule event.
- `--channel-id`: The channel ID of the schedule event.
- `--asset`: The asset of the schedule event in JSON dict format.
- `--is-loop`: Whether the schedule event is loop.
- `--duration-time-code`: The duration time code of the schedule event. Format: hh:mm:ss;ff.
## update-input-schedule-event

Options:

- `--event-id`: The ID of the input schedule event.
- `--channel-id`: The channel ID of the schedule event.
- `--live-input`: The live input of the schedule event in JSON dict format.
- `--backup-input`: The backup input of the schedule event in JSON dict format.
- `--fixed-on-air-time-utc`: The fixed on air time UTC of the schedule event. Format: hh:mm:ss.
## delete-user

Options:

- `--user-id`: The user ID of the user to be deleted.
## delete-user-content-attribute-data

Options:

- `--user-id`: The user ID of the user's content attribute data. If set to None, the user ID of the current user is used.
## delete-user-content-group-data

Options:

- `--user-id`: The user ID of the user's content group data. If set to None, the user ID of the current user is used.
## delete-user-content-security-data

Options:

- `--content-id`: The content ID of the user content security data.
- `--content-definition-id`: The content definition ID of the user content security data.
- `--user-id`: The user ID of the user's content security data. If set to None, the user ID of the current user is used.
- `--email`: The email of the user content security data.
- `--uid`: The ID of the user content security data.
- `--key-name`: The key name of the user content security data.
- `--expiration-date`: The expiration date of the user content security data.
## delete-user-data

Options:

- `--user-id`: The user ID of the user's data. If set to None, the user ID of the current user is used.
## delete-user-dislike-data

Options:

- `--user-id`: The user ID of the user's dislike data. If set to None, the user ID of the current user is used.
## delete-user-favorites-data

Options:

- `--user-id`: The user ID of the user's favorites data. If set to None, the user ID of the current user is used.
## delete-user-likes-data

Options:

- `--user-id`: The user ID of the user's likes data. If set to None, the user ID of the current user is used.
## delete-user-saved-search-data

Options:

- `--user-id`: The user ID of the user's saved search data. If set to None, the user ID of the current user is used.
## delete-user-session-data

Options:

- `--user-id`: The user ID of the user's session data. If set to None, the user ID of the current user is used.
## delete-user-share-data

Options:

- `--user-id`: The user ID of the user's share data. If set to null, the user ID of the current user is used.
## delete-user-video-tracking-data

Options:

- `--id`: The asset ID of the user video tracking data.
- `--content-id`: The content ID of the user video tracking data.
- `--video-tracking-attribute-id`: The video tracking attribute ID of the user video tracking data.
- `--user-id`: The user ID of the user video tracking data. If set to None, the user ID of the current user is used.
- `--uid`: The ID of the user video tracking data.
- `--is-first-quartile`: The first quartile of the user video tracking data.
- `--is-midpoint`: The midpoint of the user video tracking data.
- `--is-third-quartile`: The third quartile of the user video tracking data.
- `--is-complete`: The complete of the user video tracking data.
- `--is-hidden`: The hidden of the user video tracking data.
- `--is-live-stream`: The live stream of the user video tracking data.
- `--max-second`: The max second of the user video tracking data.
- `--last-second`: The last second of the user video tracking data.
- `--total-seconds`: The total seconds of the user video tracking data.
- `--last-beacon-date`: The last beacon date of the user video tracking data.
- `--key-name`: The key name of the user video tracking data.
## change-session-status

Options:

- `--user-id`: The ID of the user. If set to None, the user ID of the current user is used.
- `--user-session-status`: The status of the user session.
- `--application-id`: The application ID of the user session.
## get-user-session

Options:

- `--user-id`: The ID of the user session. If set to None, the user ID of the current user is used.
## reset-password

Options:

- `--code`: The code of the user.
- `--new-password`: The new password of the user.
## register

Options:

- `--email`: The email of the user.
- `--first-name`: The first name of the user.
- `--last-name`: The last name of the user.
- `--password`: The password of the user.
## resend-code

Options:

- `--email`: The email of the user.
## verify

Options:

- `--email`: The email of the user.
- `--code`: The code of the user.
## archive-asset

Options:

- `--id`: The ID of the asset to be archived.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
## build-media

Options:

- `--sources`: The sources of the media in JSON list format.
- `--title`: The title of the media.
- `--tags`: The tags of the media in JSON list format.
- `--collections`: The collections of the media in JSON list format.
- `--related-contents`: The related contents of the media in JSON list format.
- `--destination-folder-id`: The destination folder ID of the media.
- `--video-bitrate`: The video bitrate of the media.
- `--audio-tracks`: The audio tracks of the media in JSON list format.
## clip-asset

Options:

- `--id`: The ID of the asset to be clipped.
- `--start-time-code`: The start time code of the asset. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the asset. Format: hh:mm:ss;ff.
- `--title`: The title of the asset.
- `--output-folder-id`: The output folder ID of the asset.
- `--tags`: The tags of the asset in JSON list format.
- `--collections`: The collections of the asset in JSON list format.
- `--related-contents`: The related contents of the asset in JSON list format.
- `--video-bitrate`: The video bitrate of the asset.
- `--audio-tracks`: The audio tracks of the asset in JSON list format.
## copy-asset

Options:

- `--ids`: The ID(s
- `--urls`: The Nomad URL(s
- `--object-keys`: Object-key(s
- `--destination-folder-id`: The destination folder ID of the assets.
- `--batch-action`: The actions to be performed in JSON dict format.
- `--content-definition-id`: The content definition ID of the assets.
- `--schema-name`: The schema name of the assets.
- `--resolver-exempt`: The resolver exempt of the assets.
## create-annotation

Options:

- `--id`: The ID of the asset.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
- `--start-time-code`: The start time code of the annotation. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the annotation. Format: hh:mm:ss;ff.
- `--title`: The title of the annotation.
- `--summary`: The summary of the annotation.
- `--description`: The description of the annotation.
## create-asset-ad-break

Options:

- `--id`: The ID of the asset.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
- `--time-code`: The time code of the asset ad break. Format: hh:mm:ss;ff.
- `--tags`: The tags of the asset ad break in JSON list format.
- `--labels`: The labels of the asset ad break in JSON list format.
## create-folder-asset

Options:

- `--parent-id`: The parent asset ID for the parent folder.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
- `--display-name`: The visual name of the new folder.
## create-placeholder-asset

Options:

- `--parent-id`: The parent asset ID for the placeholder asset.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
- `--asset-name`: The visual name of the new placeholder. It can contain spaces and other characters, must contain file extension.
## create-screenshot-at-timecode

Options:

- `--id`: The ID of the asset.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
- `--time-code`: The time code of the screenshot. Format: hh:mm:ss;ff.
## delete-annotation

Options:

- `--id`: The ID of the asset of the annotation.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
- `--annotation-id`: The ID of the annotation.
## delete-asset

Options:

- `--id`: The ID of the asset to be deleted.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
## delete-asset-ad-break

Options:

- `--id`: The ID of the asset.
- `--url`: The Nomad URL of the Asset (file or folder
- `--object-key`: Object-key only of the Asset (file or folder
- `--ad-break-id`: The ID of the ad break.
## download-archive-asset

Options:

- `--ids`: The IDs of the assets to be downloaded in JSON list format.
- `--urls`: The Nomad URL(s
- `--object-keys`: Object-key(s
- `--file-name`: The file name of the archive asset.
- `--download-proxy`: The download proxy of the archive asset.
## duplicate-asset

Options:

- `--id`: The ID of the asset to be duplicated.
## get-annotations

Options:

- `--id`: The ID of the asset to get the annotations for.
## get-asset-ad-breaks

Options:

- `--id`: The ID of the asset to get the asset ad breaks for.
## get-asset-child-nodes

Options:

- `--id`: The ID of the asset to get the asset child nodes for.
- `--folder-id`: The ID of the folder the asset is in.
- `--sort-column`: The column to sort by.
- `--is-desc`: Whether the sort is descending or not.
- `--page-index`: The page index of the asset child nodes.
- `--page-size`: The page size of the asset child nodes.
## get-asset-details

Options:

- `--id`: The ID of the asset to get the details for.
## get-asset-manifest-with-cookies

Options:

- `--id`: The ID of the asset to get the manifest with cookies for.
- `--cookie-id`: The ID of the cookie.
## get-asset-metadata-summary

Options:

- `--id`: The ID of the asset to get the metadata summary for.
## get-asset-parent-folders

Options:

- `--id`: The asset ID of the current item to get the parents for.
- `--page-size`: The size of the page of folders to retrieve.
## get-asset-screenshot-details

Options:

- `--id`: The ID of the asset to get the screenshot details for.
- `--segment-id`: The ID of the segment.
- `--screenshot-id`: The ID of the screenshot.
## get-asset-segment-details

Options:

- `--id`: The ID of the asset to get the segment details for.
- `--segment-id`: The ID of the segment.
## get-user-uploads

Options:

- `--include-completed-uploads`: Whether to include completed uploads or not.
## get-user-upload-parts

Options:

- `--upload-id`: The ID of the upload to get the user upload parts for.
## import-annotations

Options:

- `--id`: The ID of the asset to import the annotations for.
- `--annotations`: The annotations to import in JSON list format.
## index-asset

Options:

- `--id`: The ID of the asset to index.
## local-restore-asset

Options:

- `--id`: The ID of the asset to local restore.
- `--profile`: The profile of the local restore.
## move-asset

Options:

- `--id`: The ID of the asset to move.
- `--destination-folder-id`: The destination folder ID of the move.
- `--name`: The name of the asset when moved.
- `--batch-action`: The batch action of the move in JSON dict format.
- `--content-definition-id`: The content definition ID of the move.
- `--schema-name`: The schema name of the move.
- `--resolver-exempt`: The resolver exempt of the move.
## records-asset-tracking-beacon

Options:

- `--id`: The ID of the asset to record the asset tracking beacon for.
- `--tracking-event`: The tracking event of the asset tracking beacon.
- `--live-channel-id`: The live channel ID of the asset tracking beacon.
- `--content-id`: Optional content ID to track along with required asset ID.
- `--second`: Second mark into the video/ad.
## register-asset

Options:

- `--id`: The ID of the asset to register.
- `--parent-id`: The ID of the parent.
- `--display-object-key`: The display object key of the register.
- `--bucket-name`: The bucket name of the register.
- `--object-key`: The object key of the register.
- `--e-tag`: The eTag of the register.
- `--tag-ids`: The tags of the register in JSON list format.
- `--collection-ids`: The collections of the register in JSON list format.
- `--related-content-ids`: The related contents of the register in JSON list format.
- `--sequencer`: The sequencer of the register.
- `--asset-status`: The asset status of the register.
- `--storage-class`: The storage class of the register.
- `--asset-type`: The asset type of the register.
- `--content-length`: The content length of the register.
- `--storage-event-name`: The storage event name of the register.
- `--created-date`: The created date of the register.
- `--storage-source-ip-address`: The storage source IP address of the register.
- `--start-media-processor`: The start media processor of the register.
- `--delete-missing-asset`: The delete missing asset of the register.
## reprocess-asset

Options:

- `--target-ids`: The target IDs of the reprocess in JSON list format.
## restore-asset

Options:

- `--id`: The ID of the asset to restore.
## share-asset

Options:

- `--id`: The ID of the asset to share.
- `--nomad-users`: The nomad users of the share in JSON list format.
- `--external-users`: The external users of the share in JSON list format.
- `--shared-duration-in-hours`: The share duration in hours of the share.
## start-workflow

Options:

- `--action-arguments`: The action arguments of the start in JSON dict format.
- `--target-ids`: The target IDs of the start in JSON list format.
## transcribe-asset

Options:

- `--id`: The ID of the asset to transcribe.
- `--transcript-id`: The ID of the transcript.
- `--transcript`: The transcript of the transcribe in JSON list format.
## update-annotation

Options:

- `--id`: The ID of the asset to update the annotation for.
- `--annotation-id`: The ID of the annotation.
- `--start-time-code`: The start time code of the annotation. Format: hh:mm:ss;ff.
- `--end-time-code`: The end time code of the annotation. Format: hh:mm:ss;ff.
- `--title`: The title of the annotation.
- `--summary`: The summary of the annotation.
- `--description`: The description of the annotation.
## update-asset-ad-break

Options:

- `--id`: The ID of the asset to update the ad break for.
- `--ad-break-id`: The ID of the ad break.
- `--time-code`: The time code of the asset ad break. Format: hh:mm:ss;ff.
- `--tags`: The tags of the asset ad break in JSON list format.
- `--labels`: The labels of the asset ad break in JSON list format.
## update-asset-language

Options:

- `--id`: The ID of the asset to update the language for.
- `--language-id`: The ID of the language.
## get-audit

Options:

- `--id`: The id of the asset to get the audit for.
