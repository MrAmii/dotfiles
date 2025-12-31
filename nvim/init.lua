-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- Setup plugins with lazy disabled
require("lazy").setup({
  {
    "sho-87/matrix.nvim",
    config = function()
      vim.cmd("colorscheme matrix")
    end
  }
}, {
  checker = { enabled = false },
  change_detection = { enabled = false },
  performance = {
    rtp = {
      disabled_plugins = {}
    }
  }
})

-- Basic settings
vim.opt.number = true
vim.opt.termguicolors = true

-- Never show lazy UI on startup
vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    vim.cmd("only")
  end
})
