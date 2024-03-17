
from .table_class import TableFile
from pydantic import BaseModel
from typing import Optional
from .deepbind_interface import DeepbindInterface, DeepBindData

DEFAULT_COLUMNS = [
    {
        "name": "id_probe",
        "index": None,
        "dtype": "str",
        "description": "The probe id.",
    },
    {
        "name": "pbm_sequence",
        "index": None,
        "dtype": "str",
        "description": "The sequence of the probe.",
        "check_type": True
    },
    {
        "name": "linker_sequence",
        "index": None,
        "dtype": "str",
        "description": "The linker sequence.",
        "check_type": False
    },
    {
        "name": "mean_signal_intensity",
        "index": None,
        "dtype": "float",
        "description": "PBM signal intensity result.",
        "check_type": False
    },
    {
        "name": "mean_background_intensity",
        "index": None,
        "dtype": "float",
        "description": "PBM background intensity result.",
        "check_type": False
    }
]




class PBMData(BaseModel):
		deepbind_data: DeepBindData
		array_design: str
		sequence_col: Optional[str] = None
		target_col: Optional[str] = None
		sequence_length: Optional[int] = None
		dropped_samples: Optional[dict] = None

class PBMFile(TableFile, DeepbindInterface):
	"""
	Description:
		DeepBind model class
	"""
	_class_data_key = 'PBM_data'
	PBM_data: PBMData = None



	def __init__(self,
					protein_name,
					array_design,
					source_organism,
					cite_source,
					sequence_length = None,
					dropped_samples = None ,**kwargs):
		# Extract and remove sequence_col and target_col from kwargs
		super().__init__(**kwargs)

		if 'PBM_data' in kwargs:
			self.PBM_data = PBMData(**kwargs['PBM_data'])
		else:
			if sequence_length is None:
				df = self.open_file()
				sequence_length = len(df['pbm_sequence'].iloc[0])
			PBM_data = {'target_col': 'mean_signal_intensity', 'sequence_length': sequence_length,
				'dropped_samples': dropped_samples,
				'sequence_col': 'pbm_sequence', 
				'array_design': array_design,
				'deepbind_data': {
									'source_organism': source_organism,
									'protein_name': protein_name,
									'cite_source': cite_source
								}
					}
			
			self.PBM_data = PBMData(**PBM_data)


	def get_sequence_col_name(self):
		return self.PBM_data.sequence_col
	
	def get_target_col_name(self):
		return self.PBM_data.target_col


	def get_seq_col(self):
		if self.PBM_data.sequence_col is None:
			self.set_target_cols(sequence_col=self.PBM_data.sequence_col,
						 target_col=self.PBM_data.target_col)
		return self.PBM_data.sequence_col
		
	def get_target_col(self):
		if self.PBM_data.sequence_col is None:
			self.set_target_cols(sequence_col=self.PBM_data.sequence_col,
						 target_col=self.PBM_data.target_col)
		return self.PBM_data.target_col
	

	def get_seq_lenth(self) -> int:
		"""
		Description:
			Returns the length of the sequences
		"""
		if self.PBM_data.seq_lenth is None:
			df = self.open_file()[self.get_seq_col()].dropna()
			self.PBM_data.seq_lenth = int(df.apply(lambda x: len(x)).value_counts().idxmax())
		return self.PBM_data.seq_lenth


	def get_experiment_details(self) -> dict:
		"""
		Description:
			Returns the experiment details
		"""
		return {'array_design' : self.PBM_data.array_design}
	

	def get_drop_samples(self):
		"""
		Description:
			Returns the dictionary of non vaild samples and thier indexes
		"""
		if self.PBM_data.dropped_samples is None:
			self.check_samples()
		return self.PBM_data.dropped_samples
	

	def get_model_data(self):
		"""
		Description:
			Returns the DF without the non vaild samples
		"""
		drop_samples = self.get_drop_samples()
		to_drop = drop_samples['no_seq'] + drop_samples['wrong_length'] + drop_samples['bad_seq']
		data =  self.open_file().drop(index=to_drop)
		return data
			
	def get_db_data(self) -> DeepBindData:
		"""
		Description:
			Returns the deepbind data
		"""
		return self.PBM_data.deepbind_data

	def check_samples(self):
		"""
		Description:
			Check if the samples are vaild,
			creates a dictionary of non vaild samples and thier indexes
		"""
		if self.PBM_data.dropped_samples is not None:
			return
		pbm_df = self.open_file()	
		seq_col = self.get_seq_col()	
		## mark samples with no sequence
		no_seq_idx = pbm_df[pbm_df[seq_col].isna()].index
		f_df = pbm_df.drop(index=no_seq_idx)
		## mark samples with wrong sequence length
		sample_length_idx = f_df[seq_col].apply(lambda x: len(x)) !=  self.get_seq_lenth()
		wrong_sample_length_idx = sample_length_idx[sample_length_idx].index
		f_df = f_df.drop(index=wrong_sample_length_idx)
		bad_seq = f_df[seq_col].apply(lambda x: not all(char in 'AGCT' for char in x.upper()))
		f_df = f_df.drop(index=f_df[bad_seq].index)
		f_df.shape
		drop_samples__dict = {"no_seq": no_seq_idx.to_list(), "wrong_length": wrong_sample_length_idx.to_list(), "bad_seq": f_df[bad_seq].index.to_list()}
		self.PBM_data.dropped_samples = drop_samples__dict
		self.to_json(self.get_path().split('.')[0] + '.json')
	
	@classmethod
	def update_table_json(cls,path):
		"""
		Description:
			Updates the table json file into pbm json
		"""
		pbm = cls.from_json(path=path)
		pbm.to_json(path=path)