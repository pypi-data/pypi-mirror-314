function GetOciTopLevelCommand_redis() {
    return 'redis'
}

function GetOciSubcommands_redis() {
    $ociSubcommands = @{
        'redis' = 'node-summary redis-cluster redis-cluster-summary work-request work-request-error work-request-log-entry'
        'redis node-summary' = 'list-redis-cluster-nodes'
        'redis redis-cluster' = 'change-compartment create delete get update'
        'redis redis-cluster-summary' = 'list-redis-clusters'
        'redis work-request' = 'cancel get list'
        'redis work-request-error' = 'list'
        'redis work-request-log-entry' = 'list-work-request-logs'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_redis() {
    $ociCommandsToLongParams = @{
        'redis node-summary list-redis-cluster-nodes' = 'all display-name from-json help limit page page-size redis-cluster-id sort-by sort-order'
        'redis redis-cluster change-compartment' = 'compartment-id from-json help if-match max-wait-seconds redis-cluster-id wait-for-state wait-interval-seconds'
        'redis redis-cluster create' = 'cluster-mode compartment-id defined-tags display-name freeform-tags from-json help max-wait-seconds node-count node-memory-in-gbs nsg-ids shard-count software-version subnet-id wait-for-state wait-interval-seconds'
        'redis redis-cluster delete' = 'force from-json help if-match max-wait-seconds redis-cluster-id wait-for-state wait-interval-seconds'
        'redis redis-cluster get' = 'from-json help redis-cluster-id'
        'redis redis-cluster update' = 'defined-tags display-name force freeform-tags from-json help if-match max-wait-seconds node-count node-memory-in-gbs nsg-ids redis-cluster-id shard-count wait-for-state wait-interval-seconds'
        'redis redis-cluster-summary list-redis-clusters' = 'all compartment-id display-name from-json help id lifecycle-state limit page page-size sort-by sort-order'
        'redis work-request cancel' = 'force from-json help if-match work-request-id'
        'redis work-request get' = 'from-json help work-request-id'
        'redis work-request list' = 'all compartment-id from-json help limit page page-size resource-id sort-by sort-order status work-request-id'
        'redis work-request-error list' = 'all from-json help limit page page-size sort-by sort-order work-request-id'
        'redis work-request-log-entry list-work-request-logs' = 'all from-json help limit page page-size sort-by sort-order work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_redis() {
    $ociCommandsToShortParams = @{
        'redis node-summary list-redis-cluster-nodes' = '? h'
        'redis redis-cluster change-compartment' = '? c h'
        'redis redis-cluster create' = '? c h'
        'redis redis-cluster delete' = '? h'
        'redis redis-cluster get' = '? h'
        'redis redis-cluster update' = '? h'
        'redis redis-cluster-summary list-redis-clusters' = '? c h'
        'redis work-request cancel' = '? h'
        'redis work-request get' = '? h'
        'redis work-request list' = '? c h'
        'redis work-request-error list' = '? h'
        'redis work-request-log-entry list-work-request-logs' = '? h'
    }
    return $ociCommandsToShortParams
}