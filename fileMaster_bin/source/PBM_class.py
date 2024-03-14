
from .table_class import TableFile
from pydantic import BaseModel
from typing import Optional


class PBMData(BaseModel):
		sequence_col: Optional[str] = None
		target_col: Optional[str] = None
		seq_lenth: Optional[int] = None
		dropped_samples: Optional[dict] = None

class PBMFile(TableFile):
	"""
	Description:
		DeepBind model class
	"""
	_class_data_key = 'PBM_data'
	PBM_data: PBMData = None



	def __init__(self, 
					target_col = None,
					seq_lenth = None,
					sequence_col = None,
					dropped_samples = None ,**kwargs):
		# Extract and remove sequence_col and target_col from kwargs
		# print("=======PBM======")
		# for k,v in kwargs.items():
		# 	print(k,':',v)
		super().__init__(**kwargs)

		if 'PBM_data' in kwargs:
			self.PBM_data = PBMData(**kwargs['PBM_data'])
		else:
			PBM_data = {'target_col': target_col, 'seq_lenth': seq_lenth,
			    'dropped_samples': dropped_samples, 'sequence_col': sequence_col}
			self.PBM_data = PBMData(**PBM_data)

			self.set_target_cols(self.PBM_data.sequence_col, self.PBM_data.target_col)


	def get_sequence_col_name(self):
		return self.PBM_data.sequence_col
	
	def get_target_col_name(self):
		return self.PBM_data.target_col

	def set_target_cols(self, sequence_col, target_col):
		"""
		Description:
			Sets the target and sequence columns
		"""
		if sequence_col is None or target_col is None:
			df= self.open_file().head()
			print(df.to_string())
			for i, col in enumerate(df.columns):
				print(i, col)
	
		# If the sequence_col is not set, get the sequence column
		if sequence_col is None:
			seq_idx  = int(input("Enter the sequence column: "))
			sequence_col = df.columns[seq_idx]
			self.PBM_data.sequence_col = sequence_col
		if target_col is None:
			target_idx = int(input("Enter the target column: "))
			target_col = df.columns[target_idx]
			self.PBM_data.target_col = target_col



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