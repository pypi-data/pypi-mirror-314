WITH recs AS (
	SELECT 
		start AS "start",
		(end - start) AS "duration",
		gridX AS "gridX",
		gridY AS "gridY",
		gridZ AS "gridZ",
		blockX AS "blockX",
		blockY AS "blockY",
		blockZ AS "blockZ",
		registersPerThread AS "regsperthread",
		staticSharedMemory AS "ssmembytes",
		dynamicSharedMemory AS "dsmembytes",
		NULL AS "bytes",
		NULL AS "srcmemkind",
		NULL AS "dstmemkind",
		NULL AS "memsetval",
		printf('%s (%d)', gpu.name, deviceId) AS "device",
		deviceId as "deviceId",
		contextId AS "context",
		greenContextId AS "greenContext",
		streamId AS "stream",
		str.value AS "name",
		correlationId AS "correlation",
		globalPid / 0x1000000 % 0x1000000 AS PID
	FROM
		CUPTI_ACTIVITY_KIND_KERNEL AS kern
	LEFT JOIN
		TARGET_INFO_GPU AS gpu
		ON gpu.id == kern.deviceId
	LEFT JOIN
		StringIds as str
		ON str.id == kern.shortName
		UNION ALL
		        SELECT
            start AS "start",
            (end - start) AS "duration",
            NULL AS "gridX",
            NULL AS "gridY",
            NULL AS "gridZ",
            NULL AS "blockX",
            NULL AS "blockY",
            NULL AS "blockZ",
            NULL AS "regsperthread",
            NULL AS "ssmembytes",
            NULL AS "dsmembytes",
            bytes AS "bytes",
            msrck.label AS "srcmemkind",
            mdstk.label AS "dstmemkind",
            NULL AS "memsetval",
            printf('%s (%d)', gpu.name, deviceId) AS "device",
			deviceId as "deviceId",
            contextId AS "context",
            greenContextId AS "greenContext",
            streamId AS "stream",
            '[CUDA memcpy ' || memopstr.label || ']' AS "name",
            correlationId AS "correlation",
			globalPid / 0x1000000 % 0x1000000 AS PID
        FROM
            CUPTI_ACTIVITY_KIND_MEMCPY AS memcpy
        LEFT JOIN
            ENUM_CUDA_MEMCPY_OPER AS memopstr
            ON memcpy.copyKind == memopstr.id
        LEFT JOIN
            ENUM_CUDA_MEM_KIND AS msrck
            ON memcpy.srcKind == msrck.id
        LEFT JOIN
            ENUM_CUDA_MEM_KIND AS mdstk
            ON memcpy.dstKind == mdstk.id
        LEFT JOIN
            TARGET_INFO_GPU AS gpu
            ON memcpy.deviceId == gpu.id
			UNION ALL
			SELECT
            start AS "start",
            (end - start) AS "duration",
            NULL AS "gridX",
            NULL AS "gridY",
            NULL AS "gridZ",
            NULL AS "blockX",
            NULL AS "blockY",
            NULL AS "blockZ",
            NULL AS "regsperthread",
            NULL AS "ssmembytes",
            NULL AS "dsmembytes",
            bytes AS "bytes",
            mk.label AS "srcmemkind",
            NULL AS "dstmemkind",
            value AS "memsetval",
            printf('%s (%d)', gpu.name, deviceId) AS "device",
			deviceId as "deviceId",
            contextId AS "context",
            greenContextId AS "greenContext",
            streamId AS "stream",
            '[CUDA memset]' AS "name",
            correlationId AS "correlation",
			globalPid / 0x1000000 % 0x1000000 AS PID
        FROM
            CUPTI_ACTIVITY_KIND_MEMSET AS memset
        LEFT JOIN
            ENUM_CUDA_MEM_KIND AS mk
            ON memset.memKind == mk.id
        LEFT JOIN
            TARGET_INFO_GPU AS gpu
            ON memset.deviceId == gpu.id
)
SELECT
	start AS "Start (ns)",
	duration AS "Duration:dur_ns",
	correlation AS "CorrID",
	gridX AS "GrdX",
	gridY AS "GrdY",
	gridZ AS "GrdZ",
	blockX AS "BlkX",
	blockY AS "BlkY",
	blockZ AS "BlkZ",
	regsperthread AS "Reg/Trd",
	ssmembytes AS "StcSMem:mem_B",
	dsmembytes AS "DymSMem:mem_B",
	bytes AS "bytes_b",
	CASE
		WHEN bytes IS NULL
			THEN NULL
		ELSE
			bytes * (1000000000 / duration)
	END AS "Throughput:thru_B",
	srcmemkind AS "SrcMemKd",
	dstmemkind AS "DstMemKd",
	device AS "Device",
	deviceId as "deviceid",
	PID AS "Pid",
	context AS "Ctx",
	NULLIF(greenContext, 0) AS "GreenCtx",
	stream AS "Strm",
	name AS "Name"
FROM recs
ORDER BY start;