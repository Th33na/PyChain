################################################################################
# Imports
import streamlit as st
import hashlib
import pandas as pd
from pychain import Record, Block, PyChain

################################################################################
# Streamlit Code

# Adds the cache decorator for Streamlit
@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

# Validate the user input
def valid_input(sender, receiver, amount):
    if sender is None or len(sender) == 0:
        return False, "Please input sender value."
    if receiver is None or len(receiver) == 0:
        return False, "Please input receiver value."  
    if amount <= 0:
        return False, "Please input amount greater than zero." 
    return True, "All good"

st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

stream_pychain = setup()

################################################################################
# Add an input area where you can get a value for `sender` from the user.
st.text_input("Sender", value="", key="sender")

# Add an input area where you can get a value for `receiver` from the user.
st.text_input("Receiver", value="", key="receiver")

# Add an input area where you can get a value for `amount` from the user.
st.number_input("Amount", key="amount", format="%.2f")

if st.button("Add Block"):
    sender = st.session_state.sender,
    receiver = st.session_state.receiver,
    amount = st.session_state.amount
    
    # Validate the user input
    valid, message = valid_input(sender, receiver, amount)
    if valid:
        prev_block = stream_pychain.chain[-1]
        prev_block_hash = prev_block.hash_block()

        # Create Record based on user input containing the `sender`, `receiver`,
        # and `amount` values
        record_input = Record(st.session_state.sender,
                              st.session_state.receiver,
                              st.session_state.amount)

        # Create `Block` consists of an attribute named `record`
        # which is set equal to a `Record`
        new_block = Block(
            record=record_input,
            creator_id=42,
            prev_hash=prev_block_hash
        )

        stream_pychain.add_block(new_block)
        st.balloons()
    else:
        st.write(message)


st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(stream_pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
stream_pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", stream_pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(stream_pychain.is_valid())
