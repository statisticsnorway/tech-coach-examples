# Example script showing how to read and verify Parquet Decimal columns in R.
#
# Run from the repository root:
#   Rscript src/decimal/verify_decimal_parquet.R

suppressPackageStartupMessages(library(arrow))

# Resolve file paths whether run from repo root or inside the src/decimal/ folder
base_dir <- if (dir.exists("src/decimal")) "src/decimal" else "."
default_parquet <- file.path(base_dir, "decimal_example.parquet")
int_parquet <- file.path(base_dir, "decimal_as_int_example.parquet")

if (!file.exists(default_parquet) || !file.exists(int_parquet)) {
  stop(
    "Parquet files not found. Run 'poetry run python src/decimal/decimal_parquet_notebook.py' first."
  )
}

cat("=== 1. Reading Parquet Files as Arrow Tables (as_data_frame = FALSE) ===\n")
# Important: By setting as_data_frame = FALSE, data stays in Arrow memory where
# exact decimal128 types are preserved (instead of converting to R's 64-bit double).
table_default <- read_parquet(default_parquet, as_data_frame = FALSE)
table_int <- read_parquet(int_parquet, as_data_frame = FALSE)

cat("\nSchema for 'decimal_example.parquet':\n")
print(table_default$schema)

cat("\n=== 2. Verifying Both Physical Formats Read Identically in R ===\n")
# Cast decimal columns to string inside Arrow to inspect exact decimal digits
belop_default_str <- as.vector(table_default$belop$cast(string()))
belop_int_str <- as.vector(table_int$belop$cast(string()))

cat("belop from decimal_example.parquet (FIXED_LEN_BYTE_ARRAY):\n")
print(belop_default_str)

cat("belop from decimal_as_int_example.parquet (INT64):\n")
print(belop_int_str)

stopifnot(identical(belop_default_str, belop_int_str))
stopifnot(belop_default_str[1] == "9007199254740992.01")
stopifnot(belop_default_str[2] == "9007199254740992.02")
stopifnot(is.na(belop_default_str[3]))
cat("SUCCESS: Both Parquet files return the exact same Decimal values!\n")

cat("\n=== 3. Comparing Arrow Decimal vs R Standard numeric (double) ===\n")
# In Arrow, the two large belop values (above 2^53) are strictly unequal:
arrow_equal <- as.vector(table_default$belop[1] == table_default$belop[2])
cat(sprintf(
  "In Arrow (decimal128):  9007199254740992.01 == 9007199254740992.02 -> %s\n",
  arrow_equal
))
stopifnot(!arrow_equal)

# If read directly into a standard R data.frame (as_data_frame = TRUE),
# R converts decimal128 to R's native 'numeric' (IEEE 754 float64), losing precision > 2^53:
df_r <- read_parquet(default_parquet, as_data_frame = TRUE)
r_num_1 <- df_r$belop[1]
r_num_2 <- df_r$belop[2]
r_equal <- (r_num_1 == r_num_2)

cat(sprintf("In R data.frame (double): %.2f og %.2f\n", r_num_1, r_num_2))
cat(sprintf(
  "In R data.frame (double): 9007199254740992.01 == 9007199254740992.02 -> %s (precision lost!)\n",
  r_equal
))

cat("\n=== 4. Exact Rounding in Arrow (ROUND_HALF_UP / HALF_TOWARDS_INFINITY) ===\n")
rounded_arrow <- call_function(
  "round",
  table_default$amount_decimal_p15,
  options = list(ndigits = 1L, round_mode = RoundMode$HALF_TOWARDS_INFINITY)
)

comparison_df <- data.frame(
  original_decimal = as.vector(table_default$amount_decimal_p15$cast(string())),
  arrow_round_half_up = as.vector(rounded_arrow$cast(string()))
)
print(comparison_df, row.names = FALSE)
stopifnot(comparison_df$arrow_round_half_up[1] == "103.60")

cat("\nAll verifications passed!\n")
