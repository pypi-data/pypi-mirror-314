from .nsys_event import NsysEvent
import os.path
from .mpi_event_encoding import *
from sqlalchemy import text

class MPIP2PSemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        if self.check_table('MPI_P2P_EVENTS') and self.check_table('MPI_START_WAIT_EVENTS'):
            with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_p2p.sql'), 'r') as query:
                self.query = text(query.read())
        else:
            self._empty = True
    def _preprocess(self):
        self._df["event_type"] = MPITYPE_PTOP
        return super()._preprocess()

class MPICollSemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        if self.check_table("MPI_COLLECTIVES_EVENTS"):
            with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_coll.sql'), 'r') as query:
                self.query = text(query.read())
        else:
            self._empty = True
    
    def _preprocess(self):
        self._df = self._df.drop(self._df[self._df["Event"].str.contains("File") ].index)
        self._df["event_type"] = MPITYPE_COLLECTIVE

class MPIOtherSemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        if self.check_table("MPI_OTHER_EVENTS"):
            with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_other.sql'), 'r') as query:
                self.query = text(query.read())
        else:
            self._empty = True
    
    def _preprocess(self):
        self._df = self._df.drop(self._df[self._df["Event"].str.contains("File") ].index)
        self._df = self._df.drop(self._df[self._df["Event"].str.contains("Win|MPI_Get|MPI_Put|Accumulate") ].index)
        self._df["event_type"] = MPITYPE_OTHER

class MPIRMASemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        if self.check_table("MPI_OTHER_EVENTS"):
            with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_other.sql'), 'r') as query:
                self.query = text(query.read())
        else:
            self._empty = True
    def _preprocess(self):
        self._df = self._df[self._df["Event"].str.contains("Win|MPI_Get|MPI_Put|Accumulate")]
        self._df["event_type"] = MPITYPE_RMA

class MPIIOPSemantic(NsysEvent):
    def __init__(self, report) -> None:
        super().__init__(report)
    
    def Setup(self):
        if self.check_table("MPI_OTHER_EVENTS") and self.check_table("MPI_COLLECTIVES_EVENTS"):
            with open(os.path.join(os.path.dirname(__file__), '../scripts/mpi_io.sql'), 'r') as query:
                self.query = text(query.read())
        else:
            self._empty = True
    
    def _preprocess(self):
        self._df = self._df[self._df["Event"].str.contains("File")]
        self._df["event_type"] = MPITYPE_IO