from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col


def lineage_data(spark: SparkSession, source_catalogs: list[str], target_catalogs: list[str] = None,
                 *, workspace_id: str) -> DataFrame:
    table_lineage_df = spark.table("system.access.table_lineage")
    source_catalogs.append(spark.catalog.currentCatalog())
    if not target_catalogs:
        target_catalogs = source_catalogs

    # Filter and select relevant columns for the first subquery
    t_df = table_lineage_df.filter(
        (col("entity_type").isin('NOTEBOOK')) &
        (col("source_table_catalog") != 'system') &
        (col("source_table_catalog").isin(*source_catalogs)) &
        (col("target_table_catalog").isin(*target_catalogs)) &
        (col("source_table_full_name").isNotNull()) &
        (col("target_table_full_name").isNotNull())
    )
    if workspace_id:
        t_df.filter(col("workspace_id") == workspace_id)

    t_df.select(
        "workspace_id",
        "entity_type",
        "entity_id",
        "entity_run_id",
        "source_table_full_name",
        "source_type",
        "target_table_full_name",
        "target_type",
        "event_time"
    ).limit(100000)

    # Read the column_lineage DataFrame
    column_lineage_df = spark.table("system.access.column_lineage")

    # Filter and select relevant columns for the second subquery
    c_df = column_lineage_df.select(
        "entity_type",
        "entity_id",
        "entity_run_id",
        "source_table_full_name",
        "source_column_name",
        "target_table_full_name",
        "target_column_name"
    )

    # Perform the left join
    result_df = t_df.join(
        c_df,
        (t_df.entity_id == c_df.entity_id) &
        (t_df.entity_run_id == c_df.entity_run_id) &
        (t_df.source_table_full_name == c_df.source_table_full_name) &
        (t_df.target_table_full_name == c_df.target_table_full_name),
        "left"
    )

    # Select the final columns
    final_df = result_df.select(
        t_df.workspace_id,
        t_df.entity_type,
        t_df.entity_id,
        t_df.entity_run_id,
        t_df.source_table_full_name,
        t_df.source_type,
        t_df.target_table_full_name,
        t_df.target_type,
        t_df.event_time,
        c_df.source_column_name,
        c_df.target_column_name
    )

    return final_df
