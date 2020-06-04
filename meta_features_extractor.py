import pandas as pd
import utils
dataset_type, datafile, feature_type, op_dir = utils.parse_args_metafeatures()

def extract_sentic_features(x, sentic_df, feature_type):
    df = pd.DataFrame(x, columns=["concept", "count"]).set_index("concept")
    merged_df = pd.merge(df, sentic_df, left_index=True, right_index=True)
    if feature_type == 'hourglass':
        drop_cols = ['primary_mood', 'secondary_mood', 'polarity_label', 'semantics1', 'semantics2', 'semantics3',
                 'semantics4', 'semantics5']
        merged_df = merged_df.drop(drop_cols, axis=1)
    for col in merged_df.columns[1:]:
        merged_df[col] *= merged_df["count"]

    result = merged_df.sum()
    result /= result["count"]
    result = result.iloc[1:]
    return result


if __name__ == "__main__":
    count_df = pd.read_pickle(datafile)
    if feature_type == 'hourglass':
        sentic_path = "meta_features_data/senticnet5_df.p"
        sentic_df = pd.read_pickle(sentic_path)
        for col in ['pleasantness_value', 'attention_value', 'sensitivity_value', 'aptitude_value', 'polarity_value']:
            sentic_df[col] = pd.to_numeric(sentic_df[col])
    elif feature_type == 'affectivespace':
        sentic_path = "meta_features_data/affectivespace.csv"
        sentic_df = pd.read_csv(sentic_path, header=None)
        sentic_df = sentic_df.set_index(sentic_df.columns[0])

    tmp = count_df["concept_count"].apply(lambda x: extract_sentic_features(x, sentic_df, feature_type))
    result = pd.concat([count_df['#AUTHID'], tmp], axis=1)
    output_file = op_dir+dataset_type+'_'+feature_type+'.csv'
    result.to_csv(output_file, index=False)